<?php
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
$data_new = $data_gmaps['routes'];
$new_data = $data_new['0'];
$pol_data = $new_data['overview_polyline'];

//polyline..
$polyline_gmaps = $pol_data['points'];


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
CURLOPT_URL => "https://dev.tollguru.com/v1/calc/route",
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
var_dump(json_decode($response, true));
// $data = var_dump(json_decode($response, true));
//print_r($data);
?>