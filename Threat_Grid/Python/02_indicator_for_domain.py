import sys
import json
import requests

CLIENT_ID = 'client-c1092fe8-4952-4e3a-92b5-64a0fb54ffb5'
CLIENT_PASSWORD = 'AhbBtIFk36de9YoSzixig6BR3Tb2FNC_tnHf-jTEb0jiL09SohdjiQ'

SESSION = requests.session()

def generate_token():
    ''' Generate a new access token and write it to disk
    '''
    url = 'https://visibility.amp.cisco.com/iroh/oauth2/token'

    headers = {'Content-Type':'application/x-www-form-urlencoded',
               'Accept':'application/json'}

    payload = {'grant_type':'client_credentials'}

    response = requests.post(url, headers=headers, auth=(CLIENT_ID, CLIENT_PASSWORD), data=payload)

    if unauthorized(response):
        sys.exit('Unable to generate new token!\nCheck your CLIENT_ID and CLIENT_PASSWORD')

    response_json = response.json()
    access_token = response_json['access_token']

    with open('threat_response_token', 'w') as token_file:
        token_file.write(access_token)

def get_token():
    ''' Get the access token from disk if it's not there generate a new one
    '''
    for i in range(2):
        while True:
            try:
                with open('threat_response_token', 'r') as token_file:
                    access_token = token_file.read()
                    return access_token
            except FileNotFoundError:
                generate_token()
            break

def inspect(observable):
    '''Inspect the provided obsrevable and determine it's type
    '''
    inspect_url = 'https://visibility.amp.cisco.com/iroh/iroh-inspect/inspect'

    access_token = get_token()

    headers = {'Authorization':'Bearer {}'.format(access_token),
               'Content-Type':'application/json',
               'Accept':'application/json'}

    inspect_payload = {'content':observable}
    inspect_payload = json.dumps(inspect_payload)

    response = SESSION.post(inspect_url, headers=headers, data=inspect_payload)
    return response

def enrich(observable):
    ''' Query the API for a observable
    '''
    enrich_url = 'https://visibility.amp.cisco.com/iroh/iroh-enrich/observe/observables'

    access_token = get_token()

    headers = {'Authorization':'Bearer {}'.format(access_token),
               'Content-Type':'application/json',
               'Accept':'application/json'}

    response = SESSION.post(enrich_url, headers=headers, data=observable)

    return response

def unauthorized(response):
    ''' Check the status code of the response
    '''
    if response.status_code == 401 or response.status_code == 400:
        return True
    return False

def check_auth(function, param):
    ''' Query the API and validate authentication was successful
        If authentication fails, generate a new token and try again
    '''
    response = function(param)
    if unauthorized(response):
        generate_token()
        return function(param)
    return response

def query(observable):
    print("Calling API with domain = " + observable)

    response = check_auth(inspect, observable)
    inspect_output = response.text
    response = check_auth(enrich, inspect_output)

    response_json = response.json()

    print("-----------------------------------------------------------------------------")
    print('{:^20}{:^35}{}'.format("Producer", "Name", "Description"))
    for module in response_json['data']:
        module_name = module['module']
        if 'indicators' in module['data'] and module['data']['indicators']['count'] > 0:
            docs = module['data']['indicators']['docs']
            for doc in docs:
                producer = doc['producer']
                name = doc['short_description']
                desription = doc['description']
                print('{:^20}{:^35}{}'.format(producer, name, desription))
    print("-----------------------------------------------------------------------------")

def main():
    # Loop forever
    while True:
        ex_value1 = 'ns1.cloud-name.ru'
        ex_value2 = 'tubepornolive.com'
        ex_value3 = 'cisco.com'

        # Print the menu
        print("""
                    Query the Indication of Compromise Feed for a Malicious Domain
                                 ACME Inc, IT Security Department
                       """)
        print("[1] Example Malicious Domain1: " + ex_value1)
        print("[2] Example Malicious Domain2: " + ex_value2)
        print("[3] Non Malicious Domain     : " + ex_value3)
        print("")

        sha256 = input("  Enter a Domain/Example Number(Leave blank to end): ")
        sha256 = sha256.strip()
        if not sha256:
            sys.exit()

        if sha256 == '1':
            sha256 = ex_value1
        elif sha256 == '2':
            sha256 = ex_value2
        elif sha256 == '3':
            sha256 = ex_value3

        query(sha256)


if __name__ == '__main__':
    main()