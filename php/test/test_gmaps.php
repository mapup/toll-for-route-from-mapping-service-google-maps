<?php
//using googlemaps API

//from & to location..
function getPolyline($from, $to){

$key = 'google.api.key';

$url = 'https://maps.googleapis.com/maps/api/directions/json?origin='.urlencode($from).'&destination='.urlencode($to).'&key='.$key.'';

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

return $polyline_gmaps;
}

//calling getPolyline function
//testing starts here...
require_once(__DIR__.'/test_location.php');
foreach ($locdata as $item) {
$polyline_gmaps = getPolyline($item['from'], $item['to']);

//using tollguru API..
$curl = curl_init();

curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);


$postdata = array(
	"source" => "gmaps",
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
				      "content-type: application/json",
				      "x-api-key: tollguru.api.key"),
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
}
?>