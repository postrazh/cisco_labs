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

# Print verbose debugging messages
IS_VERBOSE = False

def postUrlEncoded(api_session, url, payload):
    # Perform the POST request to login
    response = api_session.request("POST", url, verify=False, data=payload)

    status = response.status_code
    content = response.text

    if IS_VERBOSE:
        print('query url=' + url)
        print('  response=' + content)

    return status, content

def postJson(api_session, url, payload):

    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("POST", url, verify=False, data=json.dumps(payload), headers=request_headers)

    json_data = json.loads(response.text)

    status = response.status_code
    content = response.text

    if IS_VERBOSE:
        print('query url=' + url)
        print('  response=' + content)

    return status, content

def putJson(api_session, url, payload):

    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("PUT", url, verify=False, data=json.dumps(payload), headers=request_headers)

    json_data = json.loads(response.text)

    status = response.status_code
    content = response.text

    if IS_VERBOSE:
        print('query url=' + url)
        print('  response=' + content)

    return status, content

def getTenantId(api_session):
    # Get the list of tenants (domains) from the SMC
    url = 'https://' + SMC_HOST + '/sw-reporting/v1/tenants/'
    response = api_session.request("GET", url, verify=False)

    # If successfully able to get list of tenants (domains)
    if (response.status_code == 200):
        tenant_list = json.loads(response.content)["data"]
        tenant_id = tenant_list[0]["id"]

        return tenant_id
    return None

def tag2Id(api_session, tenant_id, tag_name):
    # Get the list of tags (host groups) from the SMC
    url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + str(tenant_id) + '/tags/'
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
    status, content = postUrlEncoded(api_session, url, login_request_data)

    if status != 200:
        print("An error has ocurred, while logging in, with the following code {}".format(status))
        exit(0)

    # Get tenant Id
    tenant_id = getTenantId(api_session)
    if tenant_id is None:
        print("Can not get a tenant Id.")
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

            subject_id = tag2Id(api_session, tenant_id, subject_host_group)
            if subject_id is not None:
                break
            print("Invalid subject host group")

        # Input the peer host group
        while True:
            peer_host_group = input("  Enter the peer host group: ")
            peer_host_group = peer_host_group.strip()
            if not peer_host_group:
                sys.exit()

            peer_id = tag2Id(api_session, tenant_id, peer_host_group)
            if peer_id is not None:
                break
            print("Invalid peer host group")

        # Add a policy
        url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + str(tenant_id) + '/policy/customEvents'
        request_data = {
            "name": policy_name,
            "summary": "When " + policy_name + ", an alarm is raised",
            "subject": {
                "tags": {
                    "excludes": [],
                    "includes": [
                        str(subject_id)
                    ]
                },
                "orientation": "either"
            },
            "peer": {
                "tags": {
                    "excludes": [],
                    "includes": [
                        str(peer_id)
                    ]
                }
            },
            "domainId": tenant_id
        }

        status, content = postJson(api_session, url, request_data)
        if (status == 200):
            print("New policy successfully added")
        else:
            print("An error has ocurred, while adding a policy, with the following code {}".format(status))
            continue

        json_data = json.loads(content)
        policy_id = json_data['data']['customSecurityEvents']['id']
        timestamp = json_data['data']['customSecurityEvents']['timestamp']

        # Enable the policy just added
        url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + \
              str(tenant_id) + '/policy/customEvents/' + \
              str(policy_id) + '/enable'
        request_data = {
            "timestamp": timestamp
        }

        status, content = putJson(api_session, url, request_data)
        if (status == 200):
            print("Enabled the policy successfully.")
        else:
            print("An error has ocurred, while enabling the policy, with the following code {}".format(status))
            continue



