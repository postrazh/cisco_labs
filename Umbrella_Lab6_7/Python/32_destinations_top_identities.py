
import sys

import requests
import json
from datetime import datetime

API_KEY = "663a91da0a2545e6ba17acf83ef01b06"
API_SECRET = "4833be4f51ff4b398ebcbe144b9239c8"

def getTopIdentities():
    url = "https://reports.api.umbrella.com/v1/organizations/2353515/destinations/update.googleapis.com/identities"

    # do GET request for the domain status and category
    req = requests.get(url, auth = (API_KEY, API_SECRET))

    # error handling if true then the request was HTTP 200, so successful
    if (req.status_code != 200):
        print("An error has ocurred with the following code %s" % req.status_code)
        sys.exit(0)

    output = req.json()

    print('{:^20}{:^20}{:^20}{:^20}'.format(
        "Origin ID",
        "Origin Type",
        "Origin Label",
        "Number of Requests"
    ))

    for item in output["identities"]:
        origin_id = item['originId']
        origin_type = item['originType']
        origin_label = item['originLabel']
        number_of_requests = item['numberOfRequests']

        print('{:^20}{:^20}{:^20}{:^20}'.format(
            origin_id,
            origin_type,
            origin_label,
            number_of_requests
        ))

def main():
    # Print the menu
    print("""
                 Umbrella - Retrieve Destinations: Top Identities Report
                             ACME Inc, IT Security Department
                   """)

    getTopIdentities()


if __name__ == '__main__':
    main()
