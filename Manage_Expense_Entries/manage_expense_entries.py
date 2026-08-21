import requests
import os
import json
import datetime
from urllib.parse import quote

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

def add_expense_entry(vehicle, date, costtype, price, currency, odometer, note, repeatinterval=0):
    """
    vehicle         Numeric Spritmonitor ID of the vehicle to add the expense to
    date            Date of the expense in format DD.MM.YYYY
    costtype        Numeric ID of the cost type, e.g. 7 for insurance. For the full list see the
                    general infos sample code
    price           Amount of money that was payed
    currency        Numeric ID of the currency, e.g. 0 for EUR, 2 for USD. For the full list see
                    the general infos sample code
    odometer        Odometer value at the time of the expense
    note            Free text note for the expense
    repeatinterval  Repeat interval in months for a recurring expense, 0 for a one-off expense

    Note that the answer only reports whether the entry was stored - it does not contain the id of
    the created entry. Read the entry back from the list to learn its id, see find_expense_entry().
    """

    if vehicle == 0:
        raise Exception("Invalid vehicle ID")

    url = (f"{SM_API_URL}/vehicle/{vehicle}/costnote.json?date={date}&costtype={costtype}"
           f"&price={price}&currencyid={currency}&odometer={odometer}&note={quote(note)}"
           f"&repeatinterval={repeatinterval}")
    return connect_to_sm_rest(url)

def update_expense_entry(vehicle, costnote, **values):
    """
    Update an existing expense entry. Every value is optional - a value that is not passed keeps
    what is currently stored for this entry, so a single field can be changed on its own.

    Accepted values are the same as for add_expense_entry(): date, costtype, price, currencyid,
    odometer, note and repeatinterval.
    """

    if vehicle == 0:
        raise Exception("Invalid vehicle ID")

    parameters = "".join([f"&{name}={quote(str(value))}" for name, value in values.items()])
    url = f"{SM_API_URL}/vehicle/{vehicle}/costnote/{costnote}.json?{parameters}"
    return connect_to_sm_rest(url)

def delete_expense_entry(vehicle, costnote):
    """
    Delete an existing expense entry. This cannot be undone.
    """

    if vehicle == 0:
        raise Exception("Invalid vehicle ID")

    url = f"{SM_API_URL}/vehicle/{vehicle}/costnote/{costnote}.delete"
    return connect_to_sm_rest(url)

def find_expense_entry(vehicle, date, note):
    """
    Look up an expense entry by its date and note, to get hold of the id that adding an entry does
    not return. Returns None if there is no such entry.
    """
    url = f"{SM_API_URL}/vehicle/{vehicle}/costsnotes.json?limit=50"
    for entry in connect_to_sm_rest(url):
        if entry['date'] == date and entry['note'] == note:
            return entry
    return None

def main():
    vehicle_Id = 0  # set vehicle ID!

    date = datetime.date.today().strftime("%d.%m.%Y")
    costtype = 7
    price = 89.4
    currencyId = 0
    odometer = 123456
    note = "Sample entry created by the Spritmonitor API sample code"

    # add a one-off expense
    add_expense_entry(vehicle_Id, date, costtype, price, currencyId, odometer, note)
    print("Expense entry added")

    # adding does not return the id, so read the entry back to get it
    entry = find_expense_entry(vehicle_Id, date, note)
    if entry is None:
        raise Exception("The entry that was just added could not be found")
    print(json.dumps(entry, indent=4, sort_keys=True))

    # turn it into an expense that repeats every 12 months and correct its price. All other
    # values of the entry stay as they are.
    update_expense_entry(vehicle_Id, entry['id'], price=99.9, repeatinterval=12)
    print("Expense entry updated")

    # remove it again, so that running this sample leaves no data behind. Comment this out if you
    # want to keep the entry.
    delete_expense_entry(vehicle_Id, entry['id'])
    print("Expense entry deleted")

if __name__ == "__main__":
    main()
