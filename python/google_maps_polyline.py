# Importing modules
import os
import requests
import json
import polyline as poly

GMAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"
GMAPS_API_KEY = os.environ.get("GMAPS_API_KEY")

TOLLGURU_API_KEY = os.environ.get("TOLLGURU_API_KEY")
TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2"
POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service"

source = "Philadelphia, PA"
destination = "New York, NY"

# Explore https://tollguru.com/toll-api-docs to get best of all the parameter that tollguru has to offer
request_parameters = {
    "vehicle": {
        "type": "2AxlesAuto",
    },
    # Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
    "departure_time": "2021-01-05T09:46:08Z",
}


def get_polyline_from_google_maps(origin, destination):
    """
    Fetching Polyline from Google for an origin and destination pair.
    Parameters
    ----------
    source : str
            Origin address
    destination : str
       Destination address
    google_maps_api_key : str
        Google map api key
    Returns
    -------
    str - Google Polyline
    """
    # origin = "New York, NY"
    # destination = "Dallas, Texas"

    # Query Google maps with Key and Source-Destination coordinates
    URL = (
        f"{GMAPS_API_URL}?origin={origin}&destination={destination}&key={GMAPS_API_KEY}"
    )

    # converting the response to json
    # you should already have this code for Google maps so far.
    response = requests.get(URL).json()
    # you will need the following code to get a polyline.
    # extracting segments of the routes
    segments = response["routes"][0]["legs"][0]["steps"]
    # you cannot concatenate individual polylines. Instead we first need #to convert the individual polylines from each of the legs to
    # geo coordinates and then convert it one big polyline for the route #and send to TollGuru API for toll as response
    # temp_list to store all coordinates
    coordinate_list = []
    for i in segments:
        coordinate_list.extend(poly.decode(i["polyline"]["points"]))
    polyline_from_google = poly.encode(coordinate_list)
    return polyline_from_google


# you send this polyline and receive tolls using following code
def get_rates_from_tollguru(polyline):
    # Tollguru request parameters
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


if __name__ == "__main__":
    # Step 1 : Get Polyline from Google
    polyline_from_google = get_polyline_from_google_maps(source, destination)

    # Step 2 : Get rates from Tollguru
    rates_from_tollguru = get_rates_from_tollguru(polyline_from_google)

    # Step 3 : Print the rates of all the available modes of payment
    if rates_from_tollguru == {}:
        print("The route doesn't have tolls")
    else:
        print(f"The rates are \n {rates_from_tollguru}")
