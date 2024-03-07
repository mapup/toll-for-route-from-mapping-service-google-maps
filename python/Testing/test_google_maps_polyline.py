# Importing modules
import json
import requests
import os
import polyline as poly

GMAPS_API_KEY = os.environ.get("GMAPS_API_KEY")
GMAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"

TOLLGURU_API_KEY = os.environ.get("TOLLGURU_API_KEY")
TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2"
POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service"

# Explore https://tollguru.com/toll-api-docs to get best of all the parameter that tollguru has to offer
request_parameters = {
    "vehicle": {
        "type": "2AxlesAuto",
    },
    # Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
    "departure_time": "2021-01-05T09:46:08Z",
}


def get_polyline_from_google_maps(source, destination):
    """Fetching Polyline from Google"""

    # Query Google maps with Key and Source-Destination coordinates
    url = (
        f"{GMAPS_API_URL}?origin={source}&destination={destination}&key={GMAPS_API_KEY}"
    )
    # converting the response to json
    response = requests.get(url).json()
    # extracting segments of the routes
    segments = response["routes"][0]["legs"][0]["steps"]
    # temp_list to store all coordinates
    coordinate_list = []
    for i in segments:
        coordinate_list.extend(poly.decode(i["polyline"]["points"]))
    polyline_from_google = poly.encode(coordinate_list)
    return polyline_from_google


def get_rates_from_tollguru(polyline):
    """Calling Tollguru API"""

    # Tollguru resquest parameters
    headers = {"Content-type": "application/json", "x-api-key": TOLLGURU_API_KEY}
    params = {
        **request_parameters,
        "source": "google",
        "polyline": polyline,  # this is the encoded polyline that we made
    }
    # Requesting Tollguru with parameters
    response_tollguru = requests.post(
        f"{TOLLGURU_API_URL}/{POLYLINE_ENDPOINT}",
        json=params,
        headers=headers,
        timeout=200,
    ).json()
    # print(response_tollguru)
    # checking for errors or printing rates
    if str(response_tollguru).find("message") == -1:
        return response_tollguru["route"]["costs"]
    else:
        raise Exception(response_tollguru["message"])


"""Testing"""
# Importing Functions
from csv import reader, writer
import time

temp_list = []
with open("testCases.csv", "r") as f:
    csv_reader = reader(f)
    for count, i in enumerate(csv_reader):
        # if count>2:
        #  break
        if count == 0:
            i.extend(
                (
                    "Input_polyline",
                    "Tollguru_Tag_Cost",
                    "Tollguru_Cash_Cost",
                    "Tollguru_QueryTime_In_Sec",
                )
            )
        else:
            try:
                polyline = get_polyline_from_google_maps(i[1], i[2])
                i.append(polyline)
            except:
                i.append("Routing Error")

            start = time.time()
            try:
                rates = get_rates_from_tollguru(polyline)
            except:
                i.append(False)
            time_taken = time.time() - start
            if rates == {}:
                i.append((None, None))
            else:
                try:
                    tag = rates["tag"]
                except:
                    tag = None
                try:
                    cash = rates["cash"]
                except:
                    cash = None
                i.extend((tag, cash))
            i.append(time_taken)
        # print(f"{len(i)}   {i}\n")
        temp_list.append(i)

with open("testCases_result.csv", "w") as f:
    writer(f).writerows(temp_list)

"""Testing Ends"""
