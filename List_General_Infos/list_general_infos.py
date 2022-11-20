import requests
import os
import json

SM_API_URL = "https://api.spritmonitor.de/v1"

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# export 'APP_TOKEN'='<your_app_token>'
bearer_token = os.environ.get("BEARER_TOKEN")
app_token = os.environ.get("APP_TOKEN")

def bearer_auth(r):
    """
    Set authorization header
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["Application-ID"] = app_token
    r.headers["User-Agent"] = "Python Spritmonitor API Access Example"
    return r

def connect_to_sm_rest(url):
    """
    Send request to Spritmonitor REST endpoint
    """
    respose = requests.request("GET", url, auth=bearer_auth)
    if respose.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                respose.status_code, respose.text
            )
        )
    return respose.json()

def get_fuelsorts():
    url = f"{SM_API_URL}/fuelsorts.json"
    fuelsorts = connect_to_sm_rest(url)
    return fuelsorts

def get_currencies():
    url = f"{SM_API_URL}/currencies.json"
    currencies = connect_to_sm_rest(url)
    return currencies

def get_quantityunits():
    url = f"{SM_API_URL}/quantityunits.json"
    quantityunits = connect_to_sm_rest(url)
    return quantityunits

def main():
    fuelsorts = get_fuelsorts()
    currencies = get_currencies()
    quantityunits = get_quantityunits()
    print(json.dumps(fuelsorts, indent=4, sort_keys=True))
    print(json.dumps(currencies, indent=4, sort_keys=True))
    print(json.dumps(quantityunits, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()