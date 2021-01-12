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
import polyline as Poly
segments=response['routes'][0]['legs'][0]['steps']
coordinate_list=[]
for i in segments:
    coordinate_list.extend(Poly.decode(i['polyline']['points']))
polyline_from_google=Poly.encode(coordinate_list)
```

```python
#Importing modules
import json
import requests
import os 
import polyline as Poly


'''Fetching Polyline from Google'''

#API key for google map
token=os.environ.get('google_api')

#Source and Destination Coordinates
#source
source = 'Newark, NJ 07114, United States'
#Destination
destination = 'Flushing, NY 11367, United States'

#Query Google maps with Key and Source-Destination coordinates
url = 'https://maps.googleapis.com/maps/api/directions/json?origin={a}&destination={b}&key={c}'.format(a=source,b=destination,c=token)

#converting the response to json
response=requests.get(url).json()

segments=response['routes'][0]['legs'][0]['steps']
coordinate_list=[]
for i in segments:
    coordinate_list.extend(Poly.decode(i['polyline']['points']))
polyline_from_google=Poly.encode(coordinate_list)

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

'''Calling Tollguru API'''

#API key for Tollguru
Tolls_Key = os.environ.get('tollguru_api')

#Tollguru querry url
Tolls_URL = 'https://dev.tollguru.com/v1/calc/route'

#Tollguru resquest parameters
headers = {
            'Content-type': 'application/json',
            'x-api-key': Tolls_Key
          }
params = {
            'source': "google",
            'polyline': polyline_from_google ,               
            'vehicleType': '2AxlesAuto',                
            'departure_time' : "2021-01-05T09:46:08Z"   
        }

#Requesting Tollguru with parameters
response_tollguru= requests.post(Tolls_URL, json=params, headers=headers).json()

#checking for errors or printing rates
if str(response_tollguru).find('message')==-1:
    print('\n The Rates Are ')
    #extracting rates from Tollguru response is no error
    print(*response_tollguru['summary']['rates'].items(),end="\n\n")
else:
    raise Exception(response_tollguru['message'])
```

The working code can be found in google_maps_polyline.py file.

## License
ISC License (ISC). Copyright 2020 &copy;TollGuru. https://tollguru.com/

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
