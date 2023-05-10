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

With this in place, make a GET request: https://maps.googleapis.com/maps/api/directions/json?origin=${source.latitude},${source.longitude}&destination=${destination.latitude},${destination.longitude}&key=${key}

### Note:
Google Maps API Response doesn't have the complete polyline for the route. 
The response includes *overview_polyline* which is an approximate (smoothed) path of the resulting directions.
We stitch the exact polyline for the whole route by piecing together polyline from each step using the code below.

```javascript

// JSON path "$..points"
const getSteps = body => body.routes
  .map(x => x.legs)
  .reduce(flatten)
  .map(x => x.steps)
  .reduce(flatten)
  .map(x => x.polyline.points)
```

```javascript
const request = require("request");
const polyline = require("polyline");

// REST API key from MapmyIndia
const key = process.env.GOOGLE_MAPS_API_KEY;
const tollguruKey = process.env.TOLLGURU_KEY;

const source = 'Dallas, TX'

const destination = 'New York, NY';

const url = `https://maps.googleapis.com/maps/api/directions/json?origin=${source}&destination=${destination}&key=${key}`;


const head = arr => arr[0]
const flatten = (arr, x) => arr.concat(x)
// JSON path "$..points"
const getPoints = body => body.routes
  .map(x => x.legs)
  .reduce(flatten)
  .map(x => x.steps)
  .reduce(flatten)
  .map(x => x.polyline.points)
  .map(x => polyline.decode(x))
  .reduce(flatten)
const getPolyline = body => polyline.encode(getPoints(JSON.parse(body)));

const getRoute = (cb) => request.get(url, cb);

const handleRoute = (e, r, body) => console.log(getPolyline(body))

getRoute(handleRoute)
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

```javascript

const tollguruUrl = 'https://apis.tollguru.com/toll/v2/complete-polyline-from-mapping-service';

const handleRoute = (e, r, body) =>  {

  console.log(body);
  const _polyline = getPolyline(body);
  console.log(_polyline);

  request.post(
    {
      url: tollguruUrl,
      headers: {
        'content-type': 'application/json',
        'x-api-key': tollguruKey
      },
      body: JSON.stringify({
        source: "google",
        polyline: _polyline,
        vehicleType: "2AxlesAuto",
        departure_time: "2021-01-05T09:46:08Z"
      })
    },
    (e, r, body) => {
      console.log(e);
      console.log(body)
    }
  )
}

getRoute(handleRoute);
```

The working code can be found in index.js file.

## License
ISC License (ISC). Copyright 2020 &copy;TollGuru. https://tollguru.com/

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
