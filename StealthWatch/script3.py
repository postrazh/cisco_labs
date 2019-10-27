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

def postUrlEncoded(api_session, url, payload):
    # Perform the POST request to login
    response = api_session.request("POST", url, verify=False, data=payload)

    status = response.status_code
    content = response.text

    print('query url=' + url)
    print('  response=' + content)

    return status, content

def postJson(api_session, url, payload):

    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("POST", url, verify=False, data=json.dumps(payload), headers=request_headers)

    json_data = json.loads(response.text)

    status = response.status_code
    content = response.text

    print('query url=' + url)
    print('  response=' + content)

    return status, content

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

def Id2tag(api_session, tenant_id, tag_id):
    # Get the list of tags (host groups) from the SMC
    url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + str(tenant_id) + '/tags/'
    response = api_session.request("GET", url, verify=False)

    if (response.status_code != 200):
        return None

    tag_name = None
    tag_list = json.loads(response.content)["data"]
    for tag in tag_list:
        if tag['id'] == tag_id:
            tag_name = tag['name']

    return tag_name

def getTenantId(api_session):
    # Get the list of tenants (domains) from the SMC
    url = 'https://' + SMC_HOST + '/sw-reporting/v1/tenants/'
    response = api_session.request("GET", url, verify=False)
    # print('query url=' + url)
    # print('  response=' + str(response))

    # If successfully able to get list of tenants (domains)
    if (response.status_code == 200):
        # Store the tenant (domain) ID as a variable to use later
        tenant_list = json.loads(response.content)["data"]
        tenant_id = tenant_list[0]["id"]

        return tenant_id
    return None

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

    # Print the menu
    print("""
                 Stealth Watch Management
              ACME Inc, IT Security Department

                Top Alarming Hosts:    
    """)

    # Get tenant Id
    tenant_id = getTenantId(api_session)
    if tenant_id is None:
        print("Can not get a tenant Id.")
        exit(0)

    # Get the list of tenants (domains) from the SMC
    url = 'https://' + SMC_HOST + '/sw-reporting/v1/tenants/' + str(tenant_id) + "/internalHosts/alarms/topHosts"
    response = api_session.request("GET", url, verify=False)

    # If failed
    if (response.status_code != 200):
        print("Get top alarming hosts failed.")
        exit(0)

    results = json.loads(response.content)["data"]["data"]

    # Filter out the valid items and print it
    print("  Ip Address\t\t\tHost Group\t\t\t\t\t\tSource Category Events")
    for item in results:
        host_groups_list = [Id2tag(api_session, tenant_id, x) for x in item['hostGroupIds']]
        host_groups = ','.join(host_groups_list)

        print(item['ipAddress'], '\t',
              host_groups, '\t',
              str(item['sourceCategoryEvents'][0]))
        # print(item)





