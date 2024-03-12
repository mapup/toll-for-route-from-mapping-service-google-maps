<?php
// Using GoogleMaps API

$GMAPS_API_KEY = getenv('GMAPS_API_KEY');
$GMAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json";

$TOLLGURU_API_KEY = getenv('TOLLGURU_API_KEY');
$TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2";
$POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service";

// From & To locations
$source = 'Philadelphia, PA';
$destination = 'New York, NY';

// Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
$request_parameters = array(
    "vehicle" => array(
        "type" => "2AxlesAuto",
    ),
    // Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
    "departure_time" => "2021-01-05T09:46:08Z",
);

// Connection
$ggle = curl_init();

curl_setopt($ggle, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($ggle, CURLOPT_SSL_VERIFYPEER, false);

curl_setopt($ggle, CURLOPT_URL, $GMAPS_API_URL.'?origin='.urlencode($source).'&destination='.urlencode($destination).'&key='.$GMAPS_API_KEY.'');
curl_setopt($ggle, CURLOPT_RETURNTRANSFER, true);

// Getting response from Google API
$response = curl_exec($ggle);
$err = curl_error($ggle);

curl_close($ggle);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo "200 : OK\n";
}

// Extracting polyline from the JSON response
$data_gmaps = json_decode($response, true);

// Polyline
$polyline_gmaps = $data_gmaps['routes']['0']['overview_polyline']['points'];


// Using TollGuru API
$curl = curl_init();

curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);


$postdata = array(
  "source" => "gmaps",
  "polyline" => $polyline_gmaps,
  ...$request_parameters,
);

// JSON encoding source and polyline to send as postfields
$encode_postData = json_encode($postdata);

curl_setopt_array($curl, array(
  CURLOPT_URL => $TOLLGURU_API_URL . "/" . $POLYLINE_ENDPOINT,
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",

  // Sending GMaps polyline to TollGuru
  CURLOPT_POSTFIELDS => $encode_postData,
  CURLOPT_HTTPHEADER => array(
    "content-type: application/json",
    "x-api-key: " . $TOLLGURU_API_KEY),
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo "200 : OK\n";
}

// Response from TollGuru
$data = var_dump(json_decode($response, true));
print_r($data);
?>
