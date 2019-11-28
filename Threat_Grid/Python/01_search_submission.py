import sys
import requests

api_key = 'jq5s3o89o82lgtslcg23bhfred'

def searchSubmission(sha256):
    print("Calling API with SHA256 = " + sha256)

    url = 'https://panacea.threatgrid.com/api/v2/search/submissions?q={}&api_key={}'.format(sha256, api_key)

    r = requests.get(url)
    # print(r.json())
    result = r.json()

    items = result["data"]["items"]

    if not items:
        print("Empty result.")
        return

    for item in items:
        print("OS : " + str(item["item"]["analysis"]["metadata"]["sandcastle_env"]["vm"]))
        print("ID : " + str(item["item"]["analysis"]["metadata"]["sandcastle_env"]["vm_id"]))


if __name__ == '__main__':
    # Loop forever
    while True:
        ex_sha256_value1 = '325cbcc44ed8989a49c1dd72992ef71c2245d1854a404724ad9a18d2cd8c4bb1'
        ex_sha256_value2 = 'bbd7075f52e936b391857b5a8b39b63daa933b8e45155119a9495d08adfc3767'

        # Print the menu
        print("""
                  Search the Submission Endpoint with the Given SHA Value
                             ACME Inc, IT Security Department
                   """)
        print("[1] Example1: " + ex_sha256_value1)
        print("[2] Example2: " + ex_sha256_value2)
        print("")

        sha256 = input("  Enter SHA256 value/Example Number(Leave blank to end): ")
        sha256 = sha256.strip()
        if not sha256:
            sys.exit()

        if sha256 == '1':
            sha256 = ex_sha256_value1
        elif sha256 == '2':
            sha256 = ex_sha256_value2

        searchSubmission(sha256)

        print("-----------------------------------------------------------------------------")

