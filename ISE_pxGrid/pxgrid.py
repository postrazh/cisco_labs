import base64
import json
import urllib.request
import ssl

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
