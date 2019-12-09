
import sys

import requests
import json
from datetime import datetime

API_KEY = "663a91da0a2545e6ba17acf83ef01b06"
API_SECRET = "4833be4f51ff4b398ebcbe144b9239c8"

def getSecurityActivity(start_time):
    url = "https://reports.api.umbrella.com/v1/organizations/2353515/security-activity"

    # params
    params = {
        'start': start_time
    }

    # do GET request for the domain status and category
    req = requests.get(url, params=params, auth = (API_KEY, API_SECRET))

    # error handling if true then the request was HTTP 200, so successful
    if (req.status_code != 200):
        print("An error has ocurred with the following code %s" % req.status_code)
        sys.exit(0)

    output = req.json()

    print('{:^30}{:^20}{:^15}{:^20}{:^25}{:^10}'.format(
        "Date Time",
        "Origin Type",
        "Origin Label",
        "External IP",
        "Destination",
        "Action"
    ))

    for item in output["requests"]:
        origin_type = item['originType']
        external_ip = item['externalIp']
        destination = item['destination']
        origin_label = item['originLabel']
        action_taken = item['actionTaken']
        datetime = item['datetime']

        print('{:^30}{:^20}{:^15}{:^20}{:^25}{:^10}'.format(
            datetime,
            origin_type,
            origin_label,
            external_ip,
            destination,
            action_taken
        ))

def main():
    # Print the menu
    print("""
                       Umbrella - Retrieve Security Activity Report
                             ACME Inc, IT Security Department
                   """)

    value = input("  Enter the Start Time in Unix-Epoch timestamp(https://www.epochconverter.com)\n"
                  "  (Enter 0 to get all the Security Activities)\n"
                  "  Start Time : ")
    value = value.strip()
    if not value:
        sys.exit()

    getSecurityActivity(value)


if __name__ == '__main__':
    main()
