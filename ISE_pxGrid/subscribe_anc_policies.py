import asyncio
from asyncio.tasks import FIRST_COMPLETED
from pxgrid import PxgridControl
from config import Config
import json
import sys
import time
from websockets import ConnectionClosed
from ws_stomp import WebSocketStomp

async def read_key():
    line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
    return

async def read_websocket(ws):
    try:
        message = await ws.stomp_read_message()
        print("message=" + json.dumps(message))
    except ConnectionClosed:
        print('Websocket connection closed')

async def subscribe_loop(config, secret, ws_url, topic):
    ws = WebSocketStomp(ws_url, config.get_node_name(), secret, config.get_ssl_context())
    await ws.connect()
    await ws.stomp_connect(pubsub_node_name)
    await ws.stomp_subscribe(topic)

    read_key_task = asyncio.create_task(read_key())
    pending = {
        read_key_task
    }

    print("press <enter> to disconnect...")
    while True:
        read_websocket_task = asyncio.create_task(read_websocket(ws))
        pending.add(read_websocket_task)

        done, pending = await asyncio.wait(pending, return_when=FIRST_COMPLETED)
        if read_key_task in done:
            await ws.stomp_disconnect()
            # wait for receipt
            await asyncio.sleep(3)
            await ws.disconnect()
            break
        else:
            print("received")


if __name__ == '__main__':
    config = Config()
    pxgrid = PxgridControl(config=config)

    while pxgrid.account_activate()['accountState'] != 'ENABLED':
        time.sleep(60)

    # lookup for session service
    service_lookup_response = pxgrid.service_lookup('com.cisco.ise.config.anc')
    service = service_lookup_response['services'][0]
    pubsub_service_name = service['properties']['wsPubsubService']
    topic = service['properties']['statusTopic']

    # lookup for pubsub service
    service_lookup_response = pxgrid.service_lookup(pubsub_service_name)
    pubsub_service = service_lookup_response['services'][0]
    pubsub_node_name = pubsub_service['nodeName']
    secret = pxgrid.get_access_secret(pubsub_node_name)['secret']
    ws_url = pubsub_service['properties']['wsUrl']

    asyncio.get_event_loop().run_until_complete(subscribe_loop(config, secret, ws_url, topic))
