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

def add_fuel_entry(vehicle, tank, date, type, odometer, trip, quantity, quantityunit, fuelsort, price, currency, attributes, streets, percent, charge_power,
                   charge_duration, charge_info):
    """
    vehicle         Numeric Spritmonitor ID of vehicle to add a fuel up
    tank            Numeric ID of tank of vehicle to add a fuel up
    date            Date of fuel up in format DD.MM.YYYY
    type            Type of fuel up, must be one of: full, notfull, first, invalid
    odometer        Odometer value of fuel up
    trip            Driven distance since last fuel up
    quantity        Amount of fuel filled up
    quantityunit    Numeric ID of quantity unit, e.g. 1 for liter, 2 for US gallon, etc. For full list see general infos sample code
    fuelsort        Fuel sort of fuel up, e.g., 1 for diesel, 6 for gasoline, etc. For full list see general infos sample code
    price           Total cost of fuel up
    currency        Numeric ID of currency, e.g., 0 for EUR, 2 for USD, etc. For full list see general infos sample code
    attributes      Combination of one tire type (wintertires,summertires,allyeartires) and one driving style (slow,normal,fast) and one or more extras (ac,heating,trailer)
    streets         Combination of city, autobahn, land
    percent         Only for electric vehicles: Specifies the charge level in percent _after_ charging, only applicable for notfull charges
    charge_power    Only for electric vehicles: Specifies the power level in kW that was used to charge the vehicle
    charge_duration Only for electric vehicles: Specifies the duration in minutes that the vehicle was charged
    charge_info     Only for electric vehicles: Specifies the current type (ac,dc) as well as the source of measurement (source_wallbox,source_vehicle)
    """

    if vehicle == 0:
        raise Exception("Invalid vehicle ID")

    url = (f"{SM_API_URL}/vehicle/{vehicle}/tank/{tank}/fueling.json?date={date}&type={type}&odometer={odometer}" 
           f"&trip={trip}&quantity={quantity}&quantityunitid={quantityunit}&fuelsortid={fuelsort}&price={price}&currencyid={currency}"
           f"&attributes={attributes}&streets={streets}&percent={percent}&charging_power={charge_power}"
           f"&charging_duration={charge_duration}&charge_info={charge_info}")
    result = connect_to_sm_rest(url)
    print(json.dumps(result))

def main():
    vehicleId = 0 
    tankId = 1
    date = "30.03.2024"
    fuel_type = "notfull"
    odometer = 123456
    trip = 500
    quantity = 50
    quantityunit = 5
    fuelsort = 19
    price = 100
    currencyId = 1
    attributes = "summertires,normal,ac"
    streets = "land"
    percent = 80
    charge_power = 11.0
    charge_duration = 195
    charge_info = "ac,source_wallbox"
    add_fuel_entry(vehicleId, tankId, date, fuel_type, odometer, trip, quantity, quantityunit, fuelsort, price, currencyId, attributes, streets, percent,
                   charge_power, charge_duration, charge_info)

if __name__ == "__main__":
    main()