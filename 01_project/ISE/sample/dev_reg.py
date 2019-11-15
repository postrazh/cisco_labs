#!/bin/python3
#Version: 0.1

import requests
import sys
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Show the program header
def print_header():
    print("%40s" % "Firepower Thread Defense Registration")
    print("%38s" % "ACME Inc. IT Security Department")
    print("\n\n")

#Get Appliance details from user input
def get_appliance_info():
    appl = {'name':'', 'ip':'', 'reg_key':''}

    print("Enter the Details of the FTD Appliance to register:\n")

    appl['name']       = input("Appliance Name: ")
    appl['ip']         = input("Appliance IP Address: ")
    appl['reg_key']    = input("Appliance Reg Key: ")

    return appl

#Generate Authentication token for FTD
def ftd_generate_token():
    auth_url='https://192.168.128.119/api/fmc_platform/v1/auth/generatetoken'

    res = requests.post(auth_url, headers={'Authentication': 'Basic Authentication'}, auth=('admin', 'WWTwwt1!'), verify=False)

    if res.status_code != 204 or not res.headers['X-auth-access-token']:
        print("Error: Failed to get X-auth-access-token")
        sys.exit(1)

    return res.headers['X-auth-access-token']

def ftd_register_device(appl, auth_token):
    reg_url = 'https://192.168.128.119/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords'

    access_policy = {'id': '000C2998-7CD8-0ed3-0000-012884901891', 'type': 'AccessPolicy'}
    reg_req = { 'name': appl['name'], 'hostName': appl['ip'], 'regKey': appl['reg_key'],
                'type':'Device', 'accessPolicy': access_policy}

    res = requests.post(reg_url, headers={'Content-Type':'application/json', 'X-auth-access-token': auth_token}, data=json.dumps(reg_req), verify=False)

    return (res.status_code == 202)

print_header()
appl = get_appliance_info()

auth_token = ftd_generate_token()
registered = ftd_register_device(appl, auth_token)
if registered:
    print("The FTD %s with %s has been registered successfully with the FMC\n" %(appl['name'], appl['ip']))
else:
    print("The FTD %s with %s FAILED to register with the FMC\n" %(appl['name'], appl['ip']))
