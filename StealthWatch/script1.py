#!/usr/bin/env python
import sys

import requests
import json
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


# Enter all authentication info
SMC_USER = "admin"
SMC_PASSWORD = "WWTwwt1!"
SMC_HOST = "192.168.128.109"
SMC_TENANT_ID = "102"

def get(api_session, url, payload):
    # Perform the POST request to login
    response = api_session.request("POST", url, verify=False, data=payload)

    status = response.status_code
    content = response.text

    print('query url=' + url)
    print('  response=' + content)

    return status, content

def post(api_session, url, payload):

    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("POST", url, verify=False, data=json.dumps(payload), headers=request_headers)

    json_data = json.loads(response.text)

    status = response.status_code
    content = response.text

    print('query url=' + url)
    print('  response=' + content)

    return status, content

if __name__ == '__main__':

    # Initialize the Requests session
    api_session = requests.Session()

    # Login
    url = "https://" + SMC_HOST + "/token/v2/authenticate"
    login_request_data = {
        "username": SMC_USER,
        "password": SMC_PASSWORD
    }
    status, content = get(api_session, url, login_request_data)

    if status != 200:
        print("An error has ocurred, while logging in, with the following code {}".format(status))
        exit(0)

    # Print the menu
    print("""
                 Stealth Watch Management
              ACME Inc, IT Security Department

        Use this interface to manage the host group.    
    """)

    # Loop forever
    while True:
        host_group_name = input("  Enter the name of host group: ")
        host_group_name = host_group_name.strip()
        if not host_group_name:
            sys.exit()

        ip_address = input("  Enter the IP address associated with the host group: ")
        ip_address = ip_address.strip()
        if not ip_address:
            sys.exit()

        # Add a tag (host group)
        url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + SMC_TENANT_ID + '/tags'
        request_data = [
            {
                "name": host_group_name,
                "location": "INSIDE",
                "ranges": [
                    ip_address,
                ],
                "parentId": 1
            }
        ]

        status, content = post(api_session, url, request_data)
        if (status == 200):
            print("New tag (host group) successfully added")
        else:
            print("An error has ocurred, while adding tags (host groups), with the following code {}".format(status))

