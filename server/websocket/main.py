from server import AsyncServer
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


server = AsyncServer(host=IP, port=8123)
asyncio.run(server.run())
