import base64
import ssl
import urllib
import json
import sys
import time
import asyncio
from asyncio.tasks import FIRST_COMPLETED
import websockets
from websockets import ConnectionClosed
from io import StringIO

class Config:
    def __init__(self):
        self.hostname = "ise24.acme.local"
        self.nodename = "xxx3"
        self.password = "ekMynr9Zu1rpqgqj"
        self.description = ""

        self.clientcert = "win7vm.acme.local_192.168.128.114.cer"
        self.clientkey = "win7vm.acme.local_192.168.128.114.key"
        self.clientkeypassword = "Cisco123"
        self.isecert = "CertificateServicesRootCA-ise24_.cer"

    def get_host_name(self):
        return self.hostname

    def get_node_name(self):
        return self.nodename

    def get_password(self):
        if self.password is not None:
            return self.password
        else:
            return ''

    def get_description(self):
        return self.description

    def get_ssl_context(self):
        context = ssl.create_default_context()
        if self.clientcert is not None:
            context.load_cert_chain(certfile=self.clientcert,
                                    keyfile=self.clientkey,
                                    password=self.clientkeypassword)
            context.load_verify_locations(cafile=self.isecert)
            return context
        return None

class StompFrame:
    def __init__(self):
        self.headers = {}
        self.command = None
        self.content = None

    def get_command(self):
        return self.command

    def set_command(self, command):
        self.command = command

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content

    def get_header(self, key):
        return self.headers[key]

    def set_header(self, key, value):
        self.headers[key] = value

    def write(self, out):
        out.write(self.command)
        out.write('\n')
        for key in self.headers:
            out.write(key)
            out.write(':')
            out.write(self.headers[key])
            out.write('\n')
        out.write('\n')
        if self.content is not None:
            out.write(self.content)
        out.write('\0')

    @staticmethod
    def parse(input):
        frame = StompFrame()
        frame.command = input.readline().rstrip('\r\n')
        for line in input:
            line = line.rstrip('\r\n')
            if line == '':
                break
            (name, value) = line.split(':')
            frame.headers[name] = value
        frame.content = input.read()[:-1]
        return frame

class WebSocketStomp:
    def __init__(self, ws_url, user, password, ssl_ctx):
        self.ws_url = ws_url
        self.user = user
        self.password = password
        self.ssl_ctx = ssl_ctx
        self.ws = None

    async def connect(self):
        b64 = base64.b64encode(
            (self.user + ':' + self.password).encode()).decode()
        self.ws = await websockets.connect(uri=self.ws_url,
                                           extra_headers={
                                               'Authorization': 'Basic ' + b64},
                                           ssl=self.ssl_ctx)

    async def stomp_connect(self, hostname):
        print('STOMP CONNECT host=' + hostname)
        frame = StompFrame()
        frame.set_command("CONNECT")
        frame.set_header('accept-version', '1.2')
        frame.set_header('host', hostname)
        out = StringIO()
        frame.write(out)
        await self.ws.send(out.getvalue().encode('utf-8'))

    async def stomp_subscribe(self, topic):
        print('STOMP SUBSCRIBE topic=' + topic)
        frame = StompFrame()
        frame.set_command("SUBSCRIBE")
        frame.set_header('destination', topic)
        frame.set_header('id', 'my-id')
        out = StringIO()
        frame.write(out)
        await self.ws.send(out.getvalue().encode('utf-8'))

    async def stomp_send(self, topic, message):
        print('STOMP SEND topic=' + topic)
        frame = StompFrame()
        frame.set_command("SEND")
        frame.set_header('destination', topic)
        frame.set_header('content-length', str(len(message)))
        frame.set_content(message)
        out = StringIO()
        frame.write(out)
        await self.ws.send(out.getvalue().encode('utf-8'))

    # only returns for MESSAGE
    async def stomp_read_message(self):
        while True:
            message = await self.ws.recv()
            s_in = StringIO(message.decode('utf-8'))
            stomp = StompFrame.parse(s_in)
            if stomp.get_command() == 'MESSAGE':
                return stomp.get_content()
            elif stomp.get_command() == 'CONNECTED':
                version = stomp.get_header('version')
                print('STOMP CONNECTED version=' + version)
            elif stomp.get_command() == 'RECEIPT':
                receipt = stomp.get_header('receipt-id')
                print('STOMP RECEIPT id=' + receipt)
            elif stomp.get_command() == 'ERROR':
                print('STOMP ERROR content=' + stomp.get_content())

    async def stomp_disconnect(self, receipt=None):
        print('STOMP DISCONNECTING...')
        frame = StompFrame()
        frame.set_command("DISCONNECT")
        if receipt is not None:
            frame.set_header('receipt', receipt)
        out = StringIO()
        frame.write(out)
        await self.ws.send(out.getvalue().encode('utf-8'))

    async def disconnect(self):
        await self.ws.close()

    def is_open(self):
        return self.ws.open

class PxgridControl:
    def __init__(self, config):
        self.config = config

    def send_rest_request(self, url_suffix, payload):
        url = 'https://' + \
            self.config.get_host_name() + \
            ':8910/pxgrid/control/' + url_suffix
        print("pxgrid url=" + url)
        json_string = json.dumps(payload)
        print('  request=' + json_string)
        rest_request = urllib.request.Request(
            url=url, data=str.encode(json_string))
        rest_request.add_header('Content-Type', 'application/json')
        rest_request.add_header('Accept', 'application/json')
        b64 = base64.b64encode((self.config.get_node_name(
        ) + ':' + self.config.get_password()).encode()).decode()
        rest_request.add_header('Authorization', 'Basic ' + b64)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            rest_response = urllib.request.urlopen(rest_request, context=self.config.get_ssl_context())
        except Exception as e:
            print(e)
            return None

        response = rest_response.read().decode()
        print('  response=' + response)
        return json.loads(response)

    def account_activate(self):
        payload = {}
        if self.config.get_description() is not None:
            payload['description'] = self.config.get_description()
        return self.send_rest_request('AccountActivate', payload)

    def service_lookup(self, service_name):
        payload = {'name': service_name}
        return self.send_rest_request('ServiceLookup', payload)

    def service_register(self, service_name, properties):
        payload = {'name': service_name, 'properties': properties}
        return self.send_rest_request('ServiceRegister', payload)

    def get_access_secret(self, peer_node_name):
        payload = {'peerNodeName': peer_node_name}
        return self.send_rest_request('AccessSecret', payload)

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
