import requests

amp_client_id = '0ed3f7a4afef01292b93'
amp_api_key = 'aa54b2a8-a21a-445d-8fe1-543c141fca6d'

def listEventTypes():
    url = 'https://api.amp.cisco.com/v1/event_types'

    request = requests.get(url, auth=(amp_client_id, amp_api_key))
    response = request.json()

    print('{:^20} {:^15}'.format('ID', 'Name', 'Description'))

    for item in response["data"]:
        print('{:^20} {:<15}'.format(item['id'], item['name']))

if __name__ == '__main__':
    print("""
               Advanced Malware Protection (AMP) - Cloud

                    List Event Types :
                    """)

    listEventTypes()