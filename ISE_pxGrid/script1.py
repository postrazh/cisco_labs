import base64
import json
import ssl
import sys
import urllib.request

# Configuration of the pxGrid client
class Config:
    def __init__(self):

        self.hostname = "ise24.acme.local"
        self.nodename = "ise24198"
        self.password = "ekMynr9Zu1rpqgqj"
        self.description = ""

        self.verbose = True

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


# pxGrid Controller
class PxgridControl:
    def __init__(self, config):
        self.config = config

    def send_rest_request(self, url_suffix, payload):
        url = 'https://' + \
              self.config.get_host_name() + \
              ':8910/pxgrid/control/' + url_suffix
        if self.config.verbose:
            print("pxgrid url=" + url)
        json_string = json.dumps(payload)
        if self.config.verbose:
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
            rest_response = urllib.request.urlopen(rest_request, context=ctx)
        except Exception as e:
            print(e)
            return None

        response = rest_response.read().decode()
        if self.config.verbose:
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


# Perform a REST call with POST method
def query(config, secret, url, payload):
    if config.verbose:
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

    status = str(rest_response.getcode())
    content = rest_response.read().decode()

    if config.verbose:
        print('  response status=' + status)
        print('  response content=' + content)

    return status, content


# Retrive all endpoints and print it to console
def retrieving_all_endpoitns():
    # Setup the pxGrid controller
    config = Config()
    pxgrid = PxgridControl(config=config)

    # Check the account status
    activate_status = pxgrid.account_activate()
    if activate_status is None or activate_status['accountState'] != 'ENABLED':
        print("ERROR: Can not connect to ISE")
        sys.exit()

    # Lookup for Adaptive Network Control configuration service
    service_lookup_response = pxgrid.service_lookup('com.cisco.ise.config.anc')
    service = service_lookup_response['services'][0]
    node_name = service['nodeName']

    # Get a secret
    secret = pxgrid.get_access_secret(node_name)['secret']

    # Call getEndpoints REST API
    url = service['properties']['restBaseUrl'] + '/getEndpoints'
    status, content = query(config, secret, url, '{}')

    # Check the REST response status
    if status != '200':
        print("API call failed! status = %s" % status)
        return

    # Print the endpoints information
    print("\t\t   Policy Name\t\t\t   MAC Address")

    content = json.loads(content)
    for item in content["endpoints"]:
        print("\t\t%s\t\t%s" % (item["policyName"], item["macAddress"]))


if __name__ == '__main__':

    # Print the menu
    print("""
            Adaptive Network Control (ANC) Visibility
              ACME Inc, IT Security Department

    Would you like to display endpoints with the ANC policy applied?    
    """)

    # Ask the choice from the user
    answer = input("     Enter Y to continue or N to cancel: ")

    if answer == "Y":
        # Retreive all the endpoints information by calling pxGrid REST API
        retrieving_all_endpoitns()
