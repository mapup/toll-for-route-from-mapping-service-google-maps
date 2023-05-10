const request = require("request");
const polyline = require("polyline");

// REST API key from MapmyIndia
const key = process.env.GOOGLE_MAPS_API_KEY;
const tollguruKey = process.env.TOLLGURU_KEY;

const source = 'Dallas, TX'

const destination = 'New York, NY';

const url = `https://maps.googleapis.com/maps/api/directions/json?origin=${source}&destination=${destination}&key=${key}`;


const head = arr => arr[0];
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

const getRoute = (cb) => request.get(url, cb);

//const handleRoute = (e, r, body) => console.log(getPolyline(body))
//getRoute(handleRoute)

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
      body: JSON.stringify({ source: "google", polyline: _polyline })
    },
    (e, r, body) => {
      console.log(e);
      console.log(body)
    }
  )
}

getRoute(handleRoute);
