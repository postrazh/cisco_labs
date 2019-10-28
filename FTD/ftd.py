
import requests

FTD_HOST = "192.168.128.124"
FTD_USER = "admin"
FTD_PASSWORD = "WWTwwt1!"

def get_access_token(host, user, passwd):
    access_token = None
    requests.packages.urllib3.disable_warnings()
    payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(user, passwd)
    auth_headers = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        response = requests.post("https://{}/api/fdm/latest/fdm/token".format(host),
                                 data=payload, verify=False, headers=auth_headers)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            print("Login successful, access_token obtained")
    except Exception as e:
        print("Unable to POST access token request: {}".format(str(e)))
    return access_token

def main():
   access_token = get_access_token(FTD_HOST, FTD_USER, FTD_PASSWORD)

if __name__ == '__main__':
    main()