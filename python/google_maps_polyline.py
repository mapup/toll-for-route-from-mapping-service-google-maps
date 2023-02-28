# Importing modules
import os
import requests
import json
import polyline as poly

# Fetching API keys for google maps and TollGuru
# API key for google map
GOOGLE_MAPS_API_KEY = "GOOGLE_API_KEY"
# API key for Tollguru
TOLLGURU_API_KEY = "TOLLGURU_API_KEY"


def get_polyline_from_google_maps(origin, destination, google_maps_api_key):
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
    URL = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_MAPS_API_KEY}'

    # converting the response to json
# you should already have this code for Google maps so far.
    response = requests.get(URL).json()
# you will need the following code to get a polyline.
    # extracting segments of the routes
    segments = response['routes'][0]['legs'][0]['steps']
# you cannot concatenate individual polylines. Instead we first need #to convert the individual polylines from each of the legs to
# geo coordinates and then convert it one big polyline for the route #and send to TollGuru API for toll as response
    # temp_list to store all coordinates
    coordinate_list = []
    for i in segments:
        coordinate_list.extend(poly.decode(i['polyline']['points']))
    polyline_from_google = poly.encode(coordinate_list)
    return (polyline_from_google)

# you send this polyline and receive tolls using following code


def get_rates_from_tollguru(polyline):
    # Tollguru query url
    TollGuru_API_URL = 'https://api.tollguru.com/v1/origin-destination-waypoints'

    # polyline = get_polyline_from_google_maps(origin="New York, NY", destination='Dallas, TX',
    #                                           google_maps_api_key=GOOGLE_MAPS_API_KEY())

    # Tollguru request parameters
    headers = {
        'Content-type': 'application/json',
        'x-api-key': TOLLGURU_API_KEY
    }
    params = {
        # Explore https://tollguru.com/toll-api-docs to get best of all the parameter that tollguru has to offer
        'source': "google",
        # this is the encoded polyline that we made
        'polyline': polyline,
        'vehicleType': '2AxlesAuto',  # '''Visit https://tollguru.com/developers/docs/#vehicle-types to know more options'''
        'departure_time': "2021-09-16T09:46:08Z"  # '''Visit https://en.wikipedia.org/wiki/Unix_time to know the time format'''
    }
    # Requesting Tollguru with parameters
    response_tollguru = requests.post(TollGuru_API_URL,
                                      json=params, headers=headers, timeout=200).json()

    # print(response_tollguru)
    # checking for errors or printing rates
    if str(response_tollguru).find('message') == -1:
        return (response_tollguru['route']['costs'])
    else:
        raise Exception(response_tollguru['message'])


if __name__ == '__main__':
    # Step 1 :Provide Source and Destination
    origin = '658 Sanford Rd, Wells, ME 04090'
    destination = '510 Alfred Rd, Biddeford, ME 04005'

    # Step 2 : Get Polyline from Google
    polyline_from_google = get_polyline_from_google_maps(
        origin, destination, GOOGLE_MAPS_API_KEY)

    # Step 3 : Get rates from Tollguru
    rates_from_tollguru = get_rates_from_tollguru(polyline_from_google)

    # Print the rates of all the available modes of payment
    if rates_from_tollguru == {}:
        print("The route doesn't have tolls")
    else:
        print(f"The rates are \n {rates_from_tollguru}")
