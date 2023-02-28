# [Google Maps](https://cloud.google.com/maps-platform/?hl=en)

### Get key to access Google Maps APIs (if you have an API key skip this)
#### Step 1: Get API Key
* Create an account to access [Google Developer API Dashboard](https://console.cloud.google.com/apis/dashboard)
* go to signup/login link https://cloud.google.com/maps-platform/?hl=en
* you may need to add Billing Account. In that case make sure you select
  Currency as USD. 
* you will need to agree to Google's Terms of Service https://developers.google.com/terms

#### Step 2: Create project
* Login to your google api dashboard
* Click on Credentials and Create Credentials ( Create Credentials > Api key ) for the above API
* [Get API Key](https://developers.google.com/maps/documentation/javascript/get-api-key)

#### Step 3: Enable API
* Go to [Google API Library](https://console.cloud.google.com/apis/library) and 
* active at least Google Maps API 
* If you prefer you can enable Places API and Geocoding API


With this in place, make a GET request:'https://maps.googleapis.com/maps/api/directions/json?origin={a}&destination={b}&key={c}'.format(a=source,b=destination,c=token)'

### Note:
Google Maps API Response doesn't have the complete polyline for the route. 
The response includes *overview_polyline* which is an approximate (smoothed) path of the resulting directions.
We stitch the exact polyline for the whole route by piecing together polyline from each step using the code below.

```python
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
```

Note:

We extracted the polyline for a route from Google Maps API

We need to send this route polyline to TollGuru API to receive toll information

## [TollGuru API](https://tollguru.com/developers/docs/)

### Get key to access TollGuru polyline API
* create a dev account to receive a free key from TollGuru https://tollguru.com/developers/get-api-key
* suggest adding `vehicleType` parameter. Tolls for cars are different than trucks and therefore if `vehicleType` is not specified, may not receive accurate tolls. For example, tolls are generally higher for trucks than cars. If `vehicleType` is not specified, by default tolls are returned for 2-axle cars. 
* Similarly, `departure_time` is important for locations where tolls change based on time-of-the-day.

the last line can be changed to following

```python
def get_rates_from_tollguru(polyline):
    # Tollguru query url
    TollGuru_API_URL = 'https://prd.tollapi.tollguru.com/v2/polyline'

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
```

The working code can be found in google_maps_polyline.py file.

## License
ISC License (ISC). Copyright 2020 &copy;TollGuru. https://tollguru.com/

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
