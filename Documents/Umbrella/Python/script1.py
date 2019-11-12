# SOLUTION SECTION #2 GET REQUEST LAB 5-HandsOn-Investigate-API-Hunting

# import necessary libraries / modules
import csv
import sys

import requests
import json
from datetime import datetime

# umbrella investigate API KEY
API_KEY = "0cad1811-f916-4976-8642-40add0e259c2"
# csv file name
CSV_FILE = 'investigate_domain.csv'


# Investigate URL
# Sample domains:
#   "internetbadguys.com"
#   "stackoverflow.com"
#   "cisco.com"
def investigateDomain(domain):
    # URL needed for the domain status and category
    investigateUrl = "https://investigate.api.umbrella.com/domains/categorization/"

    # create header for authentication
    headers = {
        'Authorization': 'Bearer ' + API_KEY
    }

    # assemble the URI, show labels give readable output
    getUrl = investigateUrl + domain + "?showLabels"

    # do GET request for the domain status and category
    req = requests.get(getUrl, headers=headers)

    # time for timestamp of verdict domain
    time = datetime.now().isoformat()

    # error handling if true then the request was HTTP 200, so successful
    if (req.status_code != 200):
        print(
                    "An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" % {
                'error': req.status_code})
        sys.exit(0)

    # retrieve status for domain
    output = req.json()
    domainOutput = output[domain]
    domainStatus = domainOutput["status"]
    # walk through different options of status

    status = "Undefined"
    if (domainStatus == -1):
        status = "Malicious"
    elif (domainStatus == 1):
        status = "Clean"

    security_categories = str(domainOutput["security_categories"])
    content_categories = str(domainOutput["content_categories"])

    return status, security_categories, content_categories

if __name__ == '__main__':

    # Print the menu
    print("""
                 Umbrella Management
              ACME Inc, IT Security Department

                Investigate a domain :""")

    print("All output will be written to " + CSV_FILE + "\n")

    # Open the csv file
    with open(CSV_FILE, 'w') as csvFile:
        writer = csv.writer(csvFile)
        # Loop forever
        while True:
            domain = input("  Enter a domain(Leave blank to end): ")
            domain = domain.strip()
            if not domain:
                sys.exit()

            status, security_categories, content_categories = investigateDomain(domain)

            print("\tStatus = %s" % status)
            print("\tSecurity Categories = %s" % security_categories)
            print("\tContent Categories = %s" % content_categories)

            # Save to a .csv file
            row = [domain, status, security_categories, content_categories]
            writer.writerow(row)

