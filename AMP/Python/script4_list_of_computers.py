import sys

import requests
from datetime import datetime, timedelta

amp_client_id = '0ed3f7a4afef01292b93'
amp_api_key = 'aa54b2a8-a21a-445d-8fe1-543c141fca6d'

def listComputers(hostname):
    url = 'https://api.amp.cisco.com/v1/computers'

    params = {
        "hostname": [
            hostname
        ]
    }
    if not hostname:
        params = None

    request = requests.get(url, auth=(amp_client_id, amp_api_key), params=params)
    response = request.json()

    print('[{:^5}]   {:^40} {:^20} {:^20} {:^20}'.format(
        "Index",
        "Host Name",
        "Operating System",
        "Internal IP",
        "External IP"
    ))

    index = 0
    for item in response["data"]:
        index = index + 1
        print('[{:^5}]   {:^40} {:^20} {:^20} {:^20}'.format(
            index,
            item['hostname'],
            item['operating_system'],
            item['internal_ips'][0],
            item['external_ip']
        ))

    print("------------------------------------------")
    index = input("Index: ")
    index = index.strip()

    if not index.isdigit():
        print("Invalid index")
        return

    index = int(index) - 1
    if not (0 <= index < len(response['data'])):
        print("Invalid index")
        return

    connector_guid = response['data'][index]['connector_guid']

    print("---------  All Activities Associated with this Computer -----------")
    # get all the activities
    url = "https://api.amp.cisco.com/v1/computers/%s/trajectory" % connector_guid
    request = requests.get(url, auth=(amp_client_id, amp_api_key), params=params)
    response = request.json()

    print('{:^30} {:^30} {:^20} {:^20}'.format(
        "Date",
        "Event Type",
        "File Type",
        "File Name"
    ))
    for item in response["data"]['events']:
        file_type = ""
        try:
            file_type = item['file']['file_type']
        except:
            pass

        file_name = ""
        try:
            file_name = item['file']['file_name']
        except:
            pass

        print('{:^30} {:^30} {:^20} {:<20}'.format(
            item['date'],
            item['event_type'],
            file_type,
            file_name
        ))

    print("---------  Vulnerabilities Observed on this Computer -----------")
    # get the vulnerabilities
    url = "https://api.amp.cisco.com/v1/computers/%s/vulnerabilities" % connector_guid
    request = requests.get(url, auth=(amp_client_id, amp_api_key), params=params)
    response = request.json()

    if not 'vulnerabilities' in response['data']:
        print("No vulnerabilites")
        return

    print('{:^30} {:^30}'.format(
        "Application",
        "Latest Date"
    ))
    for item in response["data"]['vulnerabilities']:
        print('{:^30} {:^30}'.format(
            item['application'],
            item['latest_date']
        ))

if __name__ == '__main__':
    while True:
        # Print the menu
        print("""
                       Advanced Malware Protection (AMP) - Cloud

                        List of Computers Filtered by Hostname
                        - All Activities Associated with a Particular Computer
                        - Vulnerabilities Observed on a Specific Computer
                            """)

        hostname = input("  Hostname(Leave blank for no filter): ")
        hostname = hostname.strip()

        listComputers(hostname)

        again = input(" Do you want to run again?(y/n): ")
        again = again.strip()
        if again == 'y' or again == 'Y':
            continue
        break


