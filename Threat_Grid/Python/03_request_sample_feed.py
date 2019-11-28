import sys
import json
import requests

api_key = 'jq5s3o89o82lgtslcg23bhfred'

def requestSampleFeed(file_path):
    print("Submitting the new sample feed : " + file_path)

    url = 'https://panacea.threatgrid.com/api/v2/samples'
    parameters = {'api_key': api_key}

    try:
        with open(file_path, 'rb') as sample:
            r = requests.post(url, files={'sample': sample}, params=parameters)
    except FileNotFoundError:
        print("File Not Found")
        return

    result = r.json()

    print("Submission ID : {}".format(result['data']['submission_id']))
    print(" Submitted At : {}".format(result['data']['submitted_at']))
    print("    Sample ID : {}".format(result['data']['id']))
    print("       SHA256 : {}".format(result['data']['sha256']))

def main():
    # Loop forever
    while True:
        ex_file1 = 'test_sample1.html'

        # Print the menu
        print("""
                              Request with the API for Sample Feeds
                                 ACME Inc, IT Security Department
                       """)
        print("[1] Example File1: " + ex_file1)
        print("")

        file_path = input("  Enter File Path/Example Number(Leave blank to end): ")
        file_path = file_path.strip()
        if not file_path:
            sys.exit()

        if file_path == '1':
            file_path = ex_file1

        requestSampleFeed(file_path)

if __name__ == '__main__':
    main()