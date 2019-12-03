
import sys

import requests
import json
from datetime import datetime

API_KEY = "ApiKey aeljack@yahoo.com:68b95c0ff53947aca0203c2807842e7a"

def getObservations():
    url = "https://cisco-pmatusia.obsrvbl.com/api/v3/observations/all/"

    # create header for authentication
    headers = {
        'Authorization': API_KEY
    }

    req = requests.get(url, headers=headers)

    # error handling if true then the request was HTTP 200, so successful
    if (req.status_code != 200):
        print("An error has ocurred with the following code %s" % req.status_code)
        sys.exit(0)

    output = req.json()

    print('{:^20}{:^30}{:^12}{:^12}{:^12}{:^12}{:^12}'.format(
        "Time", "Name", "Source", "Remote IP", "Remote Port", "Protocol", "Count"
    ))
    for item in output["objects"]:
        time = item['time']
        name = item['observation_name']
        source = item['source']
        remote_ip = item.get("remote_ip", "")
        remote_port = item.get("remote_port", "")
        protocol = item.get("protocol", "")
        count = item.get("count", "")

        print('{:^20}{:^30}{:^12}{:^12}{:^12}{:^12}{:^12}'.format(
            time, name, source, remote_ip, remote_port, protocol, count
        ))

def main():
    # Print the menu
    print("""
                           Stealth Watch Cloud - Get Observations
                             ACME Inc, IT Security Department
                   """)
    getObservations()

if __name__ == '__main__':
    main()
