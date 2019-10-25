import asyncio
import base64
import pathlib
import ssl
import websockets

from config import Config

user = "ise24198"
password = "Av7upxUx0wYXGwYg"
b64 = base64.b64encode(
            (user + ':' + password).encode()).decode()
config = Config()

ssl123=config.get_ssl_context()

async def hello():
    uri = "wss://ise24.acme.local:8910/pxgrid/ise/pubsub"
    ws = await websockets.connect(uri=uri,
                                      extra_headers={
                                          'Authorization': 'Basic ' + b64},
                                      ssl=ssl123)
    i = 0

asyncio.get_event_loop().run_until_complete(hello())