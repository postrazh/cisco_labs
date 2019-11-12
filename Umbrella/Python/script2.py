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
CSV_FILE = 'risk_score_domain.csv'


# Sample domains:
#   "internetbadguys.com"
#   "stackoverflow.com"
#   "cisco.com"
def getRiskScoreDomain(domain):
    # URL needed for the domain status and category
    investigateUrl = "https://investigate.api.umbrella.com/domains/risk-score/"

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

    return output

if __name__ == '__main__':

    # Print the menu
    print("""
                 Umbrella Management
              ACME Inc, IT Security Department

                Risk scores for a domain :""")

    print("All output will be written to " + CSV_FILE + "\n")

    # Open the csv file
    with open(CSV_FILE, 'w') as csvFile:
        writer = csv.writer(csvFile)

        header = ['Domain', 'Risk Score', 'Geo Popularity Score', 'Keyword Score', 'Lexical', 'Popularity 1 Day',
                  'Popularity 30 Day', 'Popularity 7 Day', 'Popularity 90 Day', 'TLD Rank Score', 'Umbrella Block Status']
        writer.writerow(header)
        # Loop forever
        while True:
            domain = input("  Enter a domain(Leave blank to end): ")
            domain = domain.strip()
            if not domain:
                sys.exit()

            output = getRiskScoreDomain(domain)

            riskScore = output["riskScore"]
            features = output["features"]

            print("\tRisk Scores = %s" % riskScore)
            print("\tGeo Popularity Score = %s" % features[0]['normalizedScore'])
            print("\tKeyword Score = %s" % features[1]['normalizedScore'])
            print("\tLexical = %s" % features[2]['normalizedScore'])
            print("\tPopularity 1 Day = %s" % features[3]['normalizedScore'])
            print("\tPopularity 30 Day = %s" % features[4]['normalizedScore'])
            print("\tPopularity 7 Day = %s" % features[5]['normalizedScore'])
            print("\tPopularity 90 Day = %s" % features[6]['normalizedScore'])
            print("\tTLD Rank Score = %s" % features[7]['normalizedScore'])
            print("\tUmbrella Block Status = %s" % features[8]['normalizedScore'])

            # Save to a .csv file
            row = [domain, riskScore]
            for item in features:
                row.append(item['normalizedScore'])
            writer.writerow(row)

