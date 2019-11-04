from datetime import datetime
import json
import requests
import base64

server = "http://192.168.128.106:6080"
api_path = "/sma/api/v2.0/reporting/mail_users_detail/"
usrPass = "admin:WWTwwt1!"

b64Val = base64.b64encode(usrPass.encode()).decode()
headers = {'Content-Type': 'application/json', "Authorization": "Basic %s" % b64Val}

now = datetime.now()
start_time = datetime(now.year - 1, now.month, now.day, 0, 0, 0).isoformat() + ".000Z"
end_time = datetime(now.year, now.month, now.day, 0, 0, 0).isoformat() + ".000Z"

payload = {"device_type": "esa",
           "startDate": start_time,
           "endDate": end_time}

url = server + api_path

try:
    # REST call with SSL verification turned off:
    response = requests.get(url, headers=headers, verify= False, params=payload)
    status_code = response.status_code
    resp = response.text
    if (status_code == 200):
        print("GET successful. Response data --> ")
        json_resp = json.loads(resp)
        print(json.dumps(json_resp, sort_keys=True, indent=4, separators=(',', ': ')))
    else:
        response.raise_for_status()
        print("Error occurred in GET --> " + resp)
except requests.exceptions.HTTPError as err:
    print("Error in connection --> " + str(err))
finally:
    if response: response.close()
