require 'HTTParty'
require 'json'
require "fast_polylines"

# Source Details
SOURCE = 'Dallas, TX'
# Destination Details
DESTINATION = 'New York, NY'

# GET Request to Google for Polyline Pieces
KEY = ENV['GOOGLEAPI_KEY']
google_url = "https://maps.googleapis.com/maps/api/directions/json?origin=#{SOURCE}&destination=#{DESTINATION}&key=#{KEY}"
RESPONSE = HTTParty.get(google_url).body
json_parsed = JSON.parse(RESPONSE)

# Decoding polyline pieces and encoding back after combining all pieces
polyline_piece = json_parsed['routes'].map { |x| x['legs'] }.flatten.map { |y| y['steps']}.flatten.map { |z| z['polyline']['points']}
coord_decoded = polyline_piece.map {|x| FastPolylines.decode(x)}.flatten(1)
google_encoded_polyline = FastPolylines.encode(coord_decoded)

# Sending POST request to TollGuru
TOLLGURU_URL = 'https://dev.tollguru.com/v1/calc/route'
TOLLGURU_KEY = ENV['TOLLGURU_KEY']
headers = {'content-type' => 'application/json', 'x-api-key' => TOLLGURU_KEY}
body = {'source' => "google", 'polyline' => google_encoded_polyline, 'vehicleType' => "2AxlesAuto", 'departure_time' => "2021-01-05T09:46:08Z"}
tollguru_response = HTTParty.post(TOLLGURU_URL,:body => body.to_json, :headers => headers, :timeout => 60)