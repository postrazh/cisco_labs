
import sys

import requests
import json
from datetime import datetime

API_KEY = "ApiKey aeljack@yahoo.com:68b95c0ff53947aca0203c2807842e7a"

def gatherTraffics(ip_address):
    url = "https://cisco-pmatusia.obsrvbl.com/api/v3/snapshots/session-data/"

    # create header for authentication
    headers = {
        'Authorization': API_KEY
    }

    # params
    params = {
        'ip': ip_address
    }

    # do GET request for the domain status and category
    req = requests.get(url, params=params, headers=headers)

    # error handling if true then the request was HTTP 200, so successful
    if (req.status_code != 200):
        print("An error has ocurred with the following code %s" % req.status_code)
        sys.exit(0)

    output = req.json()

    print('{:^20}{:^20}{:^20}{:^20}{:^20}'.format("TimeStamp",
                                                  "IP",
                                                  "Connected IP",
                                                  "Port",
                                                  "Connected IP"))
    for item in output["objects"]:
        timestamp = item['start_timestamp_utc']
        ip = item['ip']
        connected_ip = item['connected_ip']
        port = item['port']
        connected_port = item['connected_port']

        print('{:^20}{:^20}{:^20}{:^20}{:^20}'.format(timestamp, ip, connected_ip, port, connected_port))

def main():
    # Loop forever
    while True:
        ex_value1 = '192.168.128.228'

        # Print the menu
        print("""
                               Stealth Watch Cloud - Gather Traffics
                                 ACME Inc, IT Security Department
                       """)
        print("[1] Example IP1: " + ex_value1)
        print("")

        value = input("  Enter an IP address(Leave blank to end): ")
        value = value.strip()
        if not value:
            sys.exit()

        if value == '1':
            value = ex_value1

        gatherTraffics(value)

if __name__ == '__main__':
    main()
