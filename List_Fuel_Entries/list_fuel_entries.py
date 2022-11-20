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

def get_fuel_entries(vehicle_id, limit=15, offset=0):
    """
    Retrieve fuel entries from vehicle with given id
    """

    if vehicle_id == 0:
        raise Exception("Invalid vehicle ID")

    url = f"{SM_API_URL}/vehicle/{vehicle_id}/fuelings.json?limit={limit}&offset={offset}"
    entries = connect_to_sm_rest(url)
    return entries

def main():
    vehicle_Id = 0 # set vehicled ID!
    fuel_entries = get_fuel_entries(vehicle_Id)
    print(json.dumps(fuel_entries, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()