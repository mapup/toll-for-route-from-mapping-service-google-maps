require 'HTTParty'
require 'json'
require "fast_polylines"
require "cgi"

GMAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"
GMAPS_API_KEY = ENV["GOOGLE_MAPS_API_KEY"]

TOLLGURU_API_KEY = ENV["TOLLGURU_API_KEY"]
TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2"
POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service"

source = 'Philadelphia, PA'
destination = 'New York, NY'

# Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
request_parameters = {
  "vehicle": {
    "type": "2AxlesAuto",
  },
  # Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
  "departure_time": "2021-01-05T09:46:08Z",
}

google_url = "#{GMAPS_API_URL}?origin=#{CGI::escape(source)}&destination=#{CGI::escape(destination)}&key=#{GMAPS_API_KEY}"
RESPONSE = HTTParty.get(google_url).body
json_parsed = JSON.parse(RESPONSE)

# Decoding polyline pieces and encoding back after combining all pieces
polyline_piece = json_parsed['routes'].map { |x| x['legs'] }.flatten.map { |y| y['steps']}.flatten.map { |z| z['polyline']['points']}
coord_decoded = polyline_piece.map {|x| FastPolylines.decode(x)}.flatten(1)
google_encoded_polyline = FastPolylines.encode(coord_decoded)

# Sending POST request to TollGuru
TOLLGURU_URL = "#{TOLLGURU_API_URL}/#{POLYLINE_ENDPOINT}"
headers = {'content-type': 'application/json', 'x-api-key': TOLLGURU_API_KEY}
body = {
  'source': "bing",
  'polyline': google_encoded_polyline,
  **request_parameters,
}
tollguru_response = HTTParty.post(TOLLGURU_URL,:body => body.to_json, :headers => headers, :timeout => 60)
