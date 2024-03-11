const request = require("request");
const polyline = require("polyline");

const GMAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json";
const GMAPS_API_KEY = process.env.GMAPS_API_KEY;

const TOLLGURU_API_KEY = process.env.TOLLGURU_API_KEY;
const TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2";
const POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service";

const source = 'Philadelphia, PA'
const destination = 'New York, NY';

// Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
const requestParameters = {
  "vehicle": {
    "type": "2AxlesAuto",
  },
  // Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
  "departure_time": "2021-01-05T09:46:08Z",
}

const flatten = (arr, x) => arr.concat(x);

// JSON path "$..points"
const getPoints = body => body.routes
  .map(x => x.legs)
  .reduce(flatten)
  .map(x => x.steps)
  .reduce(flatten)
  .map(x => x.polyline.points)
  .map(x => polyline.decode(x))
  .reduce(flatten);

const getPolyline = body => polyline.encode(getPoints(JSON.parse(body)));

const getRoute = (cb) => request.get(`${GMAPS_API_URL}?${new URLSearchParams({
  origin: source,
  destination: destination,
  key: GMAPS_API_KEY
}).toString()}`, cb);

const tollguruUrl = `${TOLLGURU_API_URL}/${POLYLINE_ENDPOINT}`;

const handleRoute = (e, r, body) => {

  console.log(body);
  const _polyline = getPolyline(body);
  console.log(_polyline);

  request.post(
    {
      url: tollguruUrl,
      headers: {
        'content-type': 'application/json',
        'x-api-key': TOLLGURU_API_KEY
      },
      body: JSON.stringify({
        source: "google",
        polyline: _polyline,
        ...requestParameters,
      })
    },
    (e, r, body) => {
      console.log(e);
      console.log(body)
    }
  )
}

getRoute(handleRoute);
