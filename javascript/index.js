const request = require("request");

// Token from mapbox
const token = process.env.MAPBOX_TOKEN;
const tollguruKey = process.env.TOLLGURU_KEY;

// Dallas, TX
const source = {
    longitude: '-96.7970',
    latitude: '32.7767',
}

// New York, NY
const destination = {
    longitude: '-74.0060',
    latitude: '40.7128'
};

const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${source.longitude},${source.latitude};${destination.longitude},${destination.latitude}?geometries=polyline&access_token=${token}&overview=full`

const head = arr => arr[0];
// JSON path "$..geometry"
const getGeometry = body => body.routes.map(x => x.geometry);
const getPolyline = body => head(getGeometry(JSON.parse(body)));

const getRoute = (cb) => request.get(url, cb);

//const handleRoute = (e, r, body) => console.log(getPolyline(body));
//getRoute(handleRoute);

const tollguruUrl = 'https://dev.tollguru.com/v1/calc/route';

const handleRoute = (e, r, body) =>  {
  console.log(body)
  const _polyline = getPolyline(body);
  request.post(
    {
      url: tollguruUrl,
      headers: {
        'content-type': 'application/json',
        'x-api-key': tollguruKey
      },
      body: JSON.stringify({
        source: "mapbox",
        polyline: _polyline,
      })
    },
    (e, r, body) => {
      console.log(e);
      console.log(body)
    }
  )
}

getRoute(handleRoute);
