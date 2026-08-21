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

def get_costtypes():
    url = f"{SM_API_URL}/costtypes.json"
    costtypes = connect_to_sm_rest(url)
    return costtypes

def get_units():
    """
    Retrieve the units the user has configured. Every consumption value the API returns is given
    in these units, so they are needed to label the values of a statistic correctly.
    """
    url = f"{SM_API_URL}/units.json"
    units = connect_to_sm_rest(url)
    return units

def main():
    fuelsorts = get_fuelsorts()
    currencies = get_currencies()
    quantityunits = get_quantityunits()
    costtypes = get_costtypes()
    units = get_units()
    print(json.dumps(fuelsorts, indent=4, sort_keys=True))
    print(json.dumps(currencies, indent=4, sort_keys=True))
    print(json.dumps(quantityunits, indent=4, sort_keys=True))
    print(json.dumps(costtypes, indent=4, sort_keys=True))
    print(json.dumps(units, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()