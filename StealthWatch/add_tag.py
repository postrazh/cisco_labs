#!/usr/bin/env python

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

# Set the URL for SMC login
url = "https://" + SMC_HOST + "/token/v2/authenticate"

# Let's create the loginrequest data
login_request_data = {
    "username": SMC_USER,
    "password": SMC_PASSWORD
}

# Initialize the Requests session
api_session = requests.Session()

# Perform the POST request to login
response = api_session.request("POST", url, verify=False, data=login_request_data)

print('query url=' + url)
print('  response=' + response.text)

# If the login was successful
if(response.status_code == 200):

    # Set the filter with the request data
    request_data = [
        {
            "name": "Sample Threat Feed",
            "location": "OUTSIDE",
            "description": "A sample of a threat feed",
            "ranges": [
                "149.202.170.60",
                "23.129.64.101",
                "37.187.129.166",
                "91.146.121.3"
            ],
            "hostBaselines": False,
            "suppressExcludedServices": True,
            "inverseSuppression": False,
            "hostTrap": False,
            "sendToCta": False,
            "parentId": 0
        }
    ]

    # Add the new tag (host group) in the SMC
    url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + SMC_TENANT_ID + '/tags'
    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("POST", url, verify=False, data=json.dumps(request_data), headers=request_headers)

    json_data = json.loads(response.text)

    print('query url=' + url)
    print('  response=' + response.text)

    # If successfully able to add the tag (host group)
    if (response.status_code == 200):
        print("New tag (host group) successfully added")

    # If unable to add the new tag (host group)
    else:
        print("An error has ocurred, while adding tags (host groups), with the following code {}".format(response.status_code))

    # TODO : not work, can resolve by web capturing
    uri = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(uri, timeout=30, verify=False)

    print('query uri=' + uri)
    response = api_session.delete(uri, timeout=30, verify=False)

# If the login was unsuccessful
else:
        print("An error has ocurred, while logging in, with the following code {}".format(response.status_code))


