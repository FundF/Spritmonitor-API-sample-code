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

# The unit settings returned by units.json are numeric ids. Spritmonitor has no endpoint that
# resolves them, so a client that wants to label them has to know the list:
CONSUMPTION_UNITS = {
    1: "km/l", 2: "l/100km", 3: "MPG (US)", 4: "MPG (Imp)",   # fuels filled by volume
    5: "km/kg", 6: "kg/100km", 7: "mi/kg",                    # fuels filled by mass
    8: "km/kWh", 9: "kWh/100km", 10: "mi/kWh",                # electricity
}

def date_range(sdate, edate):
    """
    Build the date range parameters for the evaluations below.

    Both dates have to be given in the format DD.MM.YYYY. They are only taken into account when
    both of them are given and both match that format - otherwise Spritmonitor silently ignores
    them and the evaluation covers the whole life of the vehicle instead of returning an error.
    """
    if sdate and edate:
        return f"&sdate={sdate}&edate={edate}"
    return ""

def get_units():
    """
    Retrieve the units the user has configured. All values below are given in these units.
    """
    url = f"{SM_API_URL}/units.json"
    return connect_to_sm_rest(url)

def get_vehicle(vehicle_id):
    """
    Retrieve one vehicle out of the vehicle list of the user. Its "consumptionunit" already is the
    readable name of the unit the consumption values of this vehicle are given in, which depends
    on whether the vehicle burns fuel or charges electricity.
    """
    url = f"{SM_API_URL}/vehicles.json"
    for vehicle in connect_to_sm_rest(url):
        if vehicle['id'] == vehicle_id:
            return vehicle
    raise Exception(f"Vehicle {vehicle_id} does not belong to this user")

def get_tanks(vehicle_id):
    """
    Retrieve the tanks of the vehicle with given id
    """
    url = f"{SM_API_URL}/vehicle/{vehicle_id}/tanks.json"
    return connect_to_sm_rest(url)

def get_monthly_consumption(vehicle_id):
    """
    Retrieve the average consumption per calendar month. Always returns 12 entries - months
    without fuel ups are returned with a consumption of 0.
    """
    url = f"{SM_API_URL}/vehicle/{vehicle_id}/monthlyconsumption.json"
    return connect_to_sm_rest(url)

def get_costs_distribution(vehicle_id, sdate=None, edate=None):
    """
    Retrieve the costs of the vehicle, grouped by cost type
    """
    url = f"{SM_API_URL}/vehicle/{vehicle_id}/costsdistribution.json?{date_range(sdate, edate)}"
    return connect_to_sm_rest(url)

def get_expenses_and_refunds(vehicle_id, sdate=None, edate=None):
    """
    Retrieve the same data split into the entries that cost money and the ones that brought
    money back
    """
    url = (f"{SM_API_URL}/vehicle/{vehicle_id}/expensesandrefundsdistribution.json"
           f"?{date_range(sdate, edate)}")
    return connect_to_sm_rest(url)

def get_driven_distance(vehicle_id, sdate=None, edate=None):
    """
    Retrieve the distance the vehicle was driven in the given period.

    Remark: for hybrid vehicles this is only correct if odometer values have been entered. Without
    them the returned distance is too high, because the distances of the single tanks are counted
    twice.
    """
    url = (f"{SM_API_URL}/vehicle/{vehicle_id}/drivendistancebetweendates.json"
           f"?{date_range(sdate, edate)}")
    return connect_to_sm_rest(url)

def get_tank_details(vehicle_id, tank_id, sdate=None, edate=None):
    """
    Retrieve the consumption of a tank, broken down by the attributes that were entered with the
    single fuel ups: tires, driving style, roads, extras and fuel sorts. Only groups the user has
    actually entered data for are returned.
    """
    url = (f"{SM_API_URL}/vehicle/{vehicle_id}/tank/{tank_id}/details.json"
           f"?{date_range(sdate, edate)}")
    return connect_to_sm_rest(url)

def print_monthly_consumption(monthly_consumption, unit):
    """
    Print the monthly consumption as a small text chart, as a dashboard would plot it
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    highest = max([entry['consumption'] for entry in monthly_consumption] + [0])
    for entry in monthly_consumption:
        consumption = entry['consumption']
        bar = "#" * int(round(40 * consumption / highest)) if highest > 0 else ""
        print(f"  {months[entry['month'] - 1]}  {consumption:8.2f} {unit:<10} {bar}")

def main():
    vehicle_Id = 0  # set vehicle ID!

    if vehicle_Id == 0:
        raise Exception("Invalid vehicle ID")

    # leave both at None to evaluate the whole life of the vehicle
    sdate = None  # e.g. "01.01.2024"
    edate = None  # e.g. "31.12.2024"

    units = get_units()
    print("Units of the user:")
    print(f"  currency id : {units['currency']}")
    for quantity in ["volume", "mass", "electricity"]:
        print(f"  {quantity:<12}: {CONSUMPTION_UNITS.get(units[quantity], units[quantity])}")

    vehicle = get_vehicle(vehicle_Id)
    print(f"\nAverage consumption per calendar month "
          f"({vehicle['make']} {vehicle['model']}):")
    print_monthly_consumption(get_monthly_consumption(vehicle_Id), vehicle['consumptionunit'])

    print("\nCosts grouped by cost type:")
    for costtype in get_costs_distribution(vehicle_Id, sdate, edate):
        print(f"  {costtype['name']:<30} {costtype['costsum']:10.2f} {costtype['curname']}")

    print("\nExpenses and refunds:")
    print(json.dumps(get_expenses_and_refunds(vehicle_Id, sdate, edate), indent=4, sort_keys=True))

    print("\nDriven distance:")
    print(json.dumps(get_driven_distance(vehicle_Id, sdate, edate), indent=4, sort_keys=True))

    for tank in get_tanks(vehicle_Id):
        print(f"\nConsumption details of tank {tank['id']}:")
        print(json.dumps(get_tank_details(vehicle_Id, tank['id'], sdate, edate),
                         indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
