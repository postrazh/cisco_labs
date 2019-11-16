import sys

import requests
from datetime import datetime, timedelta

amp_client_id = '0ed3f7a4afef01292b93'
amp_api_key = 'aa54b2a8-a21a-445d-8fe1-543c141fca6d'

def displayPolicies():
    url = 'https://api.amp.cisco.com/v1/policies'

    request = requests.get(url, auth=(amp_client_id, amp_api_key))
    response = request.json()

    print('[{:^5}]   {:^30} {:^15}'.format('Index', 'Name', 'Product'))

    index = 0
    for item in response["data"]:
        index = index + 1
        print('[{:^5}]   {:<30} {:^15}'.format(
            index,
            item['name'],
            item['product'],
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

    guid = response['data'][index]['guid']

    # get the details of a particular policy
    url = "https://api.amp.cisco.com/v1/policies/" + guid
    request = requests.get(url, auth=(amp_client_id, amp_api_key))
    response = request.json()
    data = response["data"]

    print("Policy details:")
    print("Name : " + data["name"] )
    print("Guid : " + data["guid"])
    print("Product : " + data["product"])
    print("File Lists : " + str(data['file_lists']))
    print("Used in Groups : " + str(data['used_in_groups']))


if __name__ == '__main__':
    while True:
        # Print the menu
        print("""
                   Advanced Malware Protection (AMP) - Cloud
    
                Retrieve Information About a Particular Policy :
                        """)

        displayPolicies()

        again = input(" Do you want to run again?(y/n): ")
        again = again.strip()
        if again == 'y' or again == 'Y':
            continue
        break
