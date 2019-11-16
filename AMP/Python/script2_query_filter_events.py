
import requests
from datetime import datetime, timedelta

amp_client_id = '0ed3f7a4afef01292b93'
amp_api_key = 'aa54b2a8-a21a-445d-8fe1-543c141fca6d'

def queryEvents(params):
    url = 'https://api.amp.cisco.com/v1/events'

    request = requests.get(url, auth=(amp_client_id, amp_api_key), params=params)
    response = request.json()

    print('{:^20} {:^30} {:^15} {:^20}'.format('ID', 'Date', 'Disposition', 'File Path'))
    for item in response["data"]:
        file_disposition = ""
        file_path = ""
        if 'file' in item:
            if 'disposition' in item['file']:
                file_disposition = item['file']['disposition']
            if 'file_path' in item['file']:
                file_path = item['file']['file_path']
            else:
                i = 0
        else:
            k = 0

        print('{:^20} {:^30} {:^15} {:^20}'.format(
            item['id'],
            item['date'],
            file_disposition,
            file_path
        ))

    print("------------------------------------------")
    print("Total: %d results" % len(response['data']))
    print("------------------------------------------")

if __name__ == '__main__':
    while True:
        # Print the menu
        print("""
                   Advanced Malware Protection (AMP) - Cloud

                        Query and Filter Events :
                        """)

        hours = input(" Hours before(default - 20): ")
        hours = hours.strip()
        if not hours:
            hours = 20
        hours = int(hours)
        start_date = (datetime.now() - timedelta(hours=hours)).isoformat()

        event_type = input(" Event Type(default - 1090519054): ")
        event_type = event_type.strip()
        if not event_type:
            event_type = 1090519054
        event_type = int(event_type)

        params = {
            "event_type": event_type,
            "start_date": start_date
        }

        queryEvents(params)