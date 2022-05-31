try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
try:
    import ustruct as struct
except ImportError:
    import struct
import socket


class AsyncClient:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.topic = ""
        self.reader = None
        self.writer = None
        self.cb = None

    async def subscribe(self, topic):
        print("subscribe as", topic)
        self.topic = topic
        try:
            print(self.server, self.port)
            self.reader, self.writer = await asyncio.open_connection(self.server, self.port)
        except OSError as e:
            print("Cannot connet to %s on port %d" % (self.server, self.port))
            print(e)
            return False
        self.writer.write(struct.pack("!H%ds" % len(topic), len(topic), topic.encode()))
        await self.writer.drain()
        return True

    def set_callback(self, f):
        self.cb = f

    def ping(self):
        pass

    async def check_msg(self):
        assert self.writer is not None
        assert self.reader is not None
        try:
            d = await asyncio.wait_for(self.reader.read(4), timeout=1)
        except asyncio.TimeoutError:
            print("empty")
            return
        len_all, len_topic = struct.unpack("!HH", d)
        data = await self.reader.read(len_all)
        topic, msg = struct.unpack("!%ds%ds" % (len_topic, len_all - len_topic), data)
        if self.cb:
            print("callback")
            try:
                await self.cb(topic.decode(), msg.decode())
            except TypeError:
                pass

    async def publish(self, topic, msg, get_resp=True):
        assert self.writer is not None
        assert self.reader is not None
        len_sub = len(topic)
        len_data = len_sub + len(msg)
        req = struct.pack("!HH%ds" % len_data, len_data, len_sub, (topic + msg).encode())
        self.writer.write(req)
        await self.writer.drain()
        if get_resp:
            try:
                d = await asyncio.wait_for(self.reader.read(4), timeout=5)
            except asyncio.TimeoutError:
                return None, None
            len_all, len_topic = struct.unpack("!HH", d)
            data = await self.reader.read(len_all)
            resp_topic, resp_msg = struct.unpack("!%ds%ds" % (len_topic, len_all-len_topic), data)
            return resp_topic.decode(), resp_msg.decode()
        return None, None

    async def disconnect(self):
        assert self.writer is not None
        assert self.reader is not None
        self.writer.write(struct.pack("!HH", 4))
        self.writer.write(b"exit")
        self.writer.drain()
        self.writer.close()
        await self.writer.wait_closed()

    async def reconnect(self):
        assert self.topic is not None
        await self.disconnect()
        await self.subscribe(self.topic)


class UAsyncClient(AsyncClient):
    def __init__(self, server, port, *args, **kwargs):
        super().__init__(server, port, *args, **kwargs)

    async def subscribe(self, topic):
        self.sock = socket.socket()
        try:
            serv = socket.getaddrinfo(self.server, self.port)[0][-1]
            print(serv)
            self.sock.connect((self.server, self.port))
        except OSError as e:
            print('Cannot connect to %s on port %d' % (self.server, self.port))
            self.sock.close()
            return False
        self.topic = topic
        self.writer = asyncio.StreamWriter(self.sock)
        self.reader = asyncio.StreamReader(self.sock, {})
        print(self.writer, self.reader)
        self.writer.write(struct.pack("!H%ds" % len(topic), len(topic), topic.encode()))
        await self.writer.drain()
        return True
