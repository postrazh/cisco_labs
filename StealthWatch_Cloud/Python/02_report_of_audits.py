
import sys

import requests
import json
from datetime import datetime

API_KEY = "ApiKey aeljack@yahoo.com:68b95c0ff53947aca0203c2807842e7a"

def reportAudits():
    url = "https://cisco-pmatusia.obsrvbl.com/api/v3/audit/log/"

    # create header for authentication
    headers = {
        'Authorization': API_KEY
    }

    # do GET request for the domain status and category
    req = requests.get(url, headers=headers)

    # error handling if true then the request was HTTP 200, so successful
    if (req.status_code != 200):
        print("An error has ocurred with the following code %s" % req.status_code)
        sys.exit(0)

    output = req.json()

    print('{:^30}{:^25}{:^20}'.format("TimeStamp",
                                      "User",
                                      "Description"))
    for item in output["objects"]:
        timestamp = item['time']
        user = item['actor_name']
        description = item['short_text']

        print('{:^30}{:^25}{:<20}'.format(timestamp, user, description))

def main():
    ex_value1 = '192.168.128.228'

    # Print the menu
    print("""
                       Stealth Watch Cloud - Build Report of Audit
                             ACME Inc, IT Security Department
                   """)

    reportAudits()

if __name__ == '__main__':
    main()
