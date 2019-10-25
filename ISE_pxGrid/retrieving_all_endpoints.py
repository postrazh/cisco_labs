import ssl
import sys

from pxgrid import PxgridControl
from config import Config
import urllib.request
import base64
import time


def query(config, secret, url, payload):
    print('query url=' + url)
    print('  request=' + payload)

    rest_request = urllib.request.Request(url=url, data=str.encode(payload))
    rest_request.add_header('Content-Type', 'application/json')
    rest_request.add_header('Accept', 'application/json')
    b64 = base64.b64encode((config.get_node_name() + ':' + secret).encode()).decode()
    rest_request.add_header('Authorization', 'Basic ' + b64)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        rest_response = urllib.request.urlopen(rest_request, context=ctx)
    except Exception as e:
        print(e)
        return None

    print('  response status=' + str(rest_response.getcode()))
    print('  response content=' + rest_response.read().decode())

def retrieving_all_endpoitns():
    config = Config()
    pxgrid = PxgridControl(config=config)

    activate_status = pxgrid.account_activate()
    if activate_status is None or activate_status['accountState'] != 'ENABLED':
        print("ERROR: Can not connect to ISE")
        sys.exit()

    # lookup for session service
    service_lookup_response = pxgrid.service_lookup('com.cisco.ise.config.anc')
    service = service_lookup_response['services'][0]
    node_name = service['nodeName']

    secret = pxgrid.get_access_secret(node_name)['secret']

    # call getEndpoints
    url = service['properties']['restBaseUrl'] + '/getEndpoints'
    query(config, secret, url, '{}')

if __name__ == '__main__':
    retrieving_all_endpoitns()
