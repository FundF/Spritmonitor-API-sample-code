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
    response = requests.request("GET", url, auth=bearer_auth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return check_for_errors(response.json())

def check_for_errors(result):
    """
    Spritmonitor answers with HTTP status 200 even when a request was rejected. Requests that add,
    update or delete an entry report the outcome in the response body instead: "errors" is 0 when
    the entry was stored, otherwise it holds the number of rejected fields and "errormessages"
    describes them. Looking at the status code alone would mistake a rejected entry for a stored
    one, so always check the body as well.
    """
    if isinstance(result, dict) and result.get("errors"):
        raise Exception(
            "Request was rejected: {}".format(json.dumps(result.get("errormessages", {})))
        )
    return result

def get_vehicles():
    """
    Retrieve all vehicles from user
    """
    url = f"{SM_API_URL}/vehicles.json"
    vehicles = connect_to_sm_rest(url)
    return vehicles

def get_tanks(vehicle_id):
    """
    Retrieve tanks from vehicle with given id
    """
    url = f"{SM_API_URL}/vehicle/{vehicle_id}/tanks.json"
    tanks = connect_to_sm_rest(url)
    return tanks

def get_config(vehicle_id):
    """
    Retrieve the stored configuration of the vehicle with given id. In contrast to the vehicle
    list this returns the numeric ids of the configuration instead of the display names, i.e. the
    values that are needed to update the vehicle.
    """
    url = f"{SM_API_URL}/vehicle/{vehicle_id}/getconfig.json"
    config = connect_to_sm_rest(url)
    return config

def main():
    vehicles = get_vehicles()
    for vehicle in vehicles:
        tanks = get_tanks(vehicle['id'])
        config = get_config(vehicle['id'])
        print(json.dumps(vehicle, indent=4, sort_keys=True))
        print(json.dumps(tanks, indent=4, sort_keys=True))
        print(json.dumps(config, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()