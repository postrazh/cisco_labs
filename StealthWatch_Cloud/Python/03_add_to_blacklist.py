
import sys

import requests
import json
from datetime import datetime

API_KEY = "ApiKey aeljack@yahoo.com:68b95c0ff53947aca0203c2807842e7a"

def listBlackLists():
    url = "https://cisco-pmatusia.obsrvbl.com/api/v3/blacklist/domains/"

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

    print('{:^20}{:^20}{:^20}{:^20}'.format("ID",
                                            "Category",
                                            "Name",
                                            "List On"))
    for item in output["objects"]:
        id = item['id']
        category = item['category']
        name = item['identifier']
        list_on = item['list_on']

        print('{:^20}{:^20}{:^20}{:^20}'.format(id, category, name, list_on))

def addToBlackList(domain):
    url = "https://cisco-pmatusia.obsrvbl.com/api/v3/blacklist/domains/"

    # create header for authentication
    headers = {
        'Authorization': API_KEY
    }

    # payload
    payload = {
        'category': 'domain',
        'identifier': domain,
        'list_on': 'blacklist'
    }

    # do GET request for the domain status and category
    req = requests.post(url, data=payload, headers=headers)

    # error handling if true then the request was HTTP 200, so successful
    if (req.status_code != 201):
        print("An error has ocurred with the following code %s" % req.status_code)
        sys.exit(0)

def main():
    # Loop forever
    while True:

        # Print the menu
        print("""
                             Stealth Watch Cloud - Add to the Black List
                                 ACME Inc, IT Security Department
                       """)

        listBlackLists()

        value = input("  Enter a domain to add to Black List(Leave blank to end): ")
        value = value.strip()
        if not value:
            sys.exit()

        addToBlackList(value)

if __name__ == '__main__':
    main()
