#!/usr/bin/env python
import datetime
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

def login(api_session, url, payload):
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

def put(api_session, url, payload):

    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("PUT", url, verify=False, data=json.dumps(payload), headers=request_headers)

    json_data = json.loads(response.text)

    status = response.status_code
    content = response.text

    print('query url=' + url)
    print('  response=' + content)

    return status, content

def tag2Id(api_session, tag_name):
    # Get the list of tags (host groups) from the SMC
    url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + SMC_TENANT_ID + '/tags/'
    response = api_session.request("GET", url, verify=False)

    if (response.status_code != 200):
        return None

    tag_id = None
    tag_list = json.loads(response.content)["data"]
    for tag in tag_list:
        if tag['name'] == tag_name:
            tag_id = tag['id']

    return tag_id

if __name__ == '__main__':

    # Initialize the Requests session
    api_session = requests.Session()

    # Login
    url = "https://" + SMC_HOST + "/token/v2/authenticate"
    login_request_data = {
        "username": SMC_USER,
        "password": SMC_PASSWORD
    }
    status, content = login(api_session, url, login_request_data)

    if status != 200:
        print("An error has ocurred, while logging in, with the following code {}".format(status))
        exit(0)

    # Print the menu
    print("""
                 Stealth Watch Management
              ACME Inc, IT Security Department

            Use this interface to create a policy.    
    """)

    # Loop forever
    while True:
        policy_name = input("  Enter the name of policy: ")
        policy_name = policy_name.strip()
        if not policy_name:
            sys.exit()

        while True:
            subject_host_group = input("  Enter the subject host group: ")
            subject_host_group = subject_host_group.strip()
            if not subject_host_group:
                sys.exit()

            subject_id = tag2Id(subject_host_group)
            if subject_id is not None:
                break
            print("Invalid subject host group")

        # Input the peer host group
        while True:
            peer_host_group = input("  Enter the peer host group: ")
            peer_host_group = peer_host_group.strip()
            if not peer_host_group:
                sys.exit()

            peer_id = tag2Id(peer_host_group)
            if peer_id is not None:
                break
            print("Invalid peer host group")

        # Add a policy
        url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + SMC_TENANT_ID + '/policy/customEvents'
        request_data = [
            {
                "name": policy_name,
                "summary": "When " + policy_name + ", an alarm is raised",
                "subject": {
                    "tags": {
                        "excludes": [],
                        "includes": [
                            subject_id
                        ]
                    },
                    "orientation": "either"
                },
                "peer": {
                    "tags": {
                        "excludes": [],
                        "includes": [
                            peer_id
                        ]
                    }
                },
                "domainId": SMC_TENANT_ID
            }
        ]

        status, content = post(api_session, url, request_data)
        if (status == 200):
            print("New tag (host group) successfully added")
        else:
            print("An error has ocurred, while adding tags (host groups), with the following code {}".format(status))

        policy_id = 23;

        # Enable the policy just added
        datetime = datetime.datetime.utcnow()
        timestamp = datetime.strftime('%Y-%m-%dT%H:%M:%S.000')

        url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + SMC_TENANT_ID + '/policy/customEvents/' + peer_id + '/enable'
        request_data = { "timestamp": timestamp }

        status, content = post(api_session, url, request_data)
        if (status == 200):
            print("New tag (host group) successfully added")
        else:
            print("An error has ocurred, while adding tags (host groups), with the following code {}".format(status))