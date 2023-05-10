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

```php

//extracting polyline from the JSON response..
$data_gmaps = json_decode($response, true);

//polyline..
$polyline_gmaps = $data_gmaps['routes']['0']['overview_polyline']['points'];


```

```php
//using googlemaps API

//from & to location..
$from = 'Mainstr,Dallas,TX';
$to = 'Addison,TX';
$key = 'googleapi_key';

$url = 'https://maps.googleapis.com/maps/api/directions/json?origin='.$from.'&destination='.$to.'&key='.$key.'';

//connection..
$ggle = curl_init();

curl_setopt($ggle, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($ggle, CURLOPT_SSL_VERIFYPEER, false);

curl_setopt($ggle, CURLOPT_URL, $url);
curl_setopt($ggle, CURLOPT_RETURNTRANSFER, true);

//getting response from googleapis..
$response = curl_exec($ggle);
$err = curl_error($ggle);

curl_close($ggle);

if ($err) {
	  echo "cURL Error #:" . $err;
} else {
	  echo "200 : OK\n";
}

//extracting polyline from the JSON response..
$data_gmaps = json_decode($response, true);

//polyline..
$polyline_gmaps = $data_gmaps['routes']['0']['overview_polyline']['points'];

```

Note:

We extracted the polyline for a route from Google Maps API

We need to send this route polyline to TollGuru API to receive toll information

## [TollGuru API](https://tollguru.com/developers/docs/)

### Get key to access TollGuru polyline API
* create a dev account to receive a free key from TollGuru https://tollguru.com/developers/get-api-key
* suggest adding `vehicleType` parameter. Tolls for cars are different than trucks and therefore if `vehicleType` is not specified, may not receive accurate tolls. For example, tolls are generally higher for trucks than cars. If `vehicleType` is not specified, by default tolls are returned for 2-axle cars. 
* Similarly, `departure_time` is important for locations where tolls change based on time-of-the-day and it can be passed in `$postdata` array.

the last line can be changed to following

```php
//using tollguru API..
$curl = curl_init();

curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);


$postdata = array(
	"source" => "google",
	"polyline" => $polyline_gmaps
);

//json encoding source and polyline to send as postfields..
$encode_postData = json_encode($postdata);

curl_setopt_array($curl, array(
CURLOPT_URL => "https://apis.tollguru.com/toll/v2/complete-polyline-from-mapping-service",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "POST",


//sending gmaps polyline to tollguru
CURLOPT_POSTFIELDS => $encode_postData,
CURLOPT_HTTPHEADER => array(
    "content-type: application/json"
    "x-api-key: tollguruapi_key"),
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
	  echo "cURL Error #:" . $err;
} else {
	  echo "200 : OK\n";
}

//response from tollguru..
$data = var_dump(json_decode($response, true));
print_r($data);

```

The working code can be found in `php_curl_gmaps.php` file.

## License
ISC License (ISC). Copyright 2020 &copy;TollGuru. https://tollguru.com/

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.