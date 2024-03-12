<?php
// Using GoogleMaps API

$GMAPS_API_KEY = getenv('GMAPS_API_KEY');
$GMAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json";

$TOLLGURU_API_KEY = getenv('TOLLGURU_API_KEY');
$TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2";
$POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service";

// Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
$request_parameters = array(
  "vehicle" => array(
    "type" => "2AxlesAuto",
  ),
  // Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
  "departure_time" => "2021-01-05T09:46:08Z",
);

// From and To locations
function getPolyline($from, $to) {
  global $GMAPS_API_KEY, $GMAPS_API_URL;

  // Connection
  $ggle = curl_init();

  curl_setopt($ggle, CURLOPT_SSL_VERIFYHOST, false);
  curl_setopt($ggle, CURLOPT_SSL_VERIFYPEER, false);

  curl_setopt($ggle, CURLOPT_URL, $GMAPS_API_URL.'?origin='.urlencode($from).'&destination='.urlencode($to).'&key='.$GMAPS_API_KEY.'');
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
  //polyline..
  $polyline_gmaps = $data_gmaps['routes']['0']['overview_polyline']['points'];

  return $polyline_gmaps;
}

// Calling getPolyline function
// Testing starts here
require_once(__DIR__.'/test_location.php');
foreach ($locdata as $item) {
  $polyline_gmaps = getPolyline($item['from'], $item['to']);

  // Using tollguru API
  $curl = curl_init();

  curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
  curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);


  $postdata = array(
    "source" => "gmaps",
    "polyline" => $polyline_gmaps,
    ...$request_parameters
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
  $data = json_decode($response, true);

  $tag = $data['route']['costs']['tag'];
  $cash = $data['route']['costs']['cash'];

  $dumpFile = fopen("dump.txt", "a") or die("unable to open file!");
  fwrite($dumpFile, "from =>");
  fwrite($dumpFile, $item['from'].PHP_EOL);
  fwrite($dumpFile, "to =>");
  fwrite($dumpFile, $item['to'].PHP_EOL);
  fwrite($dumpFile, "polyline =>".PHP_EOL);
  fwrite($dumpFile, $polyline_gmaps.PHP_EOL);
  fwrite($dumpFile, "tag =>");
  fwrite($dumpFile, $tag.PHP_EOL);
  fwrite($dumpFile, "cash =>");
  fwrite($dumpFile, $cash.PHP_EOL);
  fwrite($dumpFile, "*************************************************************************".PHP_EOL);
  echo 'from: '.$item['from'].' to '.$item['to'].'';
  echo "\n";
  echo "tag = ";
  print_r($data['route']['costs']['tag']);
  echo "\ncash = ";
  print_r($data['route']['costs']['cash']);
  echo "\n";
  echo "**************************************************************************\n";
  // Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
  $request_parameters = array(
    "vehicle" => array(
      "type" => "2AxlesAuto",
    ),
    // Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
    "departure_time" => "2021-01-05T09:46:08Z",
  );
}
?>
