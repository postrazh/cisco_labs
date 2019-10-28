import json
import sys

import requests

FTD_HOST = "192.168.128.124"
FTD_USER = "admin"
FTD_PASSWORD = "WWTwwt1!"

def get_access_token(host, user, passwd):
    access_token = None
    requests.packages.urllib3.disable_warnings()
    payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(user, passwd)
    auth_headers = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        response = requests.post("https://{}/api/fdm/latest/fdm/token".format(host),
                                 data=payload, verify=False, headers=auth_headers)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
    except Exception as e:
        print("Unable to POST access token request: {}".format(str(e)))
    return access_token

def get_security_zones(host, access_token):
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    url = 'api/fdm/v3/object/securityzones'
    response = requests.get('https://{host}/{url}'.format(host=host, url=url),
                            verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET security zones {} {}".format(response.status_code, response.json()))
        return None

    return response.json()

def add_security_zone(host, access_token, zone_name):
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    state = None
    url = 'api/fdm/v3/object/securityzones'
    payload = {
        "type": "securityzone",
        "mode": "ROUTED",
        "name": str(zone_name),
        "interfaces": []
    }

    response = requests.post('https://{host}/{url}'.format(host=host, url=url),
                             data=json.dumps(payload), verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed in adding a security zone {} {}".format(response.status_code, response.json()))
    else:
        state = response.json().get('state')
        print(state)

    return state

def post_deployment(host, access_token):
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    url = 'api/fdm/latest/operational/deploy'
    response = requests.post('https://{host}/{url}'.format(host=host, url=url), verify=False,
                             headers=headers)
    if response.status_code != 200:
        print("Failed POST deploy response {} {}".format(response.status_code, response.json()))
    else:
        print(response.json())
        name = response.json().get('name')
        print(name)
        print("Deployment will take a few minutes.")

def main():
    # Print the menu
    print("""
                    Firepower Threat Defense
                 ACME Inc, IT Security Department

           Use this interface to manage security zones on FTD.    
       """)

    access_token = get_access_token(FTD_HOST, FTD_USER, FTD_PASSWORD)

    # Get and print the security zones
    security_zones = get_security_zones(FTD_HOST, access_token)
    print(security_zones)

    # Add a new security zone
    zone_name = input("  Enter the name of security zone: ")
    zone_name = zone_name.strip()
    if not zone_name:
        sys.exit()

    add_security_zone(FTD_HOST, access_token, zone_name)

    # Post deployment
    post_deployment(FTD_HOST, access_token)

if __name__ == '__main__':
    main()