import usocket as socket
import uasyncio as asyncio
import uselect as select
import ustruct as struct
from machine import Pin


class AsyncServer:

    def __init__(self, host='0.0.0.0', port=8123, backlog=5, timeout=20):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout
        self.writers = {}

    async def run(self):
        print(self.host, self.port)
        self.server = await asyncio.start_server(self.got_connect, self.host, self.port, self.backlog)
        print('Awaiting client connection')
        led = Pin(2, Pin.OUT)
        while True:
            value = not led.value()
            led.value(value)
            await asyncio.sleep(1)

    async def got_connect(self, reader, writer):
        topic_len = await reader.read(2)
        topic_len = topic_len[0] << 8 | topic_len[1]
        data = await reader.read(topic_len)
        topic = data.decode()
        self.writers[topic] = writer
        addr = writer.get_extra_info('peername')
        print('Got connection from client', repr(addr), "topic", topic)
        try:
            while True:
                data_len = await reader.read(4)
                if data_len == b'':
                    break
                len_all, len_topic = struct.unpack("!HH", data_len)
                data = await reader.read(len_all)
                if data == b'exit':
                    break
                unpack = struct.unpack("!%ds%ds" % (len_topic, len_all-len_topic), data)
                sub_topic = unpack[0].decode()
                msg = unpack[1].decode()
                if sub_topic in self.writers:
                    w = self.writers[sub_topic]
                    l_topic = len(topic)
                    l_data = l_topic + len(msg)
                    w.write(struct.pack("!HH%ds" % l_data, l_data, l_topic, (topic + msg).encode()))
                    await w.drain()
                    print("Send data \"%s\" form %s to %s" % (msg, topic, sub_topic))
                else:
                    print(sub_topic, "did not subscribe")
                    writer.write(struct.pack("!HH30s", 30, 6, b"serverdevice did not subscribe"))
                    await writer.drain()
        except OSError:
            pass
        self.writers.pop(topic, None)
        await reader.wait_closed()
        print(topic, "closed connection")

    async def close(self):
        print('Closing server')
        self.server.close()
        await self.server.wait_closed()
        print('Server closed.')
