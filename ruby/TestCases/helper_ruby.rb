require 'HTTParty'
require 'json'
require "fast_polylines"
require 'cgi'

GMAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"
GMAPS_API_KEY = ENV["GOOGLE_MAPS_API_KEY"]

TOLLGURU_API_KEY = ENV["TOLLGURU_API_KEY"]
TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2"
POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service"

# Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
request_parameters = {
  "vehicle": {
    "type": "2AxlesAuto",
  },
  # Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
  "departure_time": "2021-01-05T09:46:08Z",
}

def get_toll_rate(source_val,dest_val)
    # Source Details
    source = source_val
    # Destination Details
    destination = dest_val

    # GET Request to Google for Polyline Pieces
    google_url = "#{GMAPS_API_URL}?origin=#{CGI::escape(source)}&destination=#{CGI::escape(destination)}&key=#{GMAPS_API_KEY}"
    response = HTTParty.get(google_url)
    json_parsed = JSON.parse(response.body)

    # Decoding polyline pieces and encoding back after combining all pieces
    polyline_piece = json_parsed['routes'].map { |x| x['legs'] }.flatten.map { |y| y['steps']}.flatten.map { |z| z['polyline']['points']}
    coord_decoded = polyline_piece.map {|x| FastPolylines.decode(x)}.flatten(1)
    google_encoded_polyline = FastPolylines.encode(coord_decoded)

    # Sending POST request to TollGuru
    tollguru_url = "#{TOLLGURU_API_URL}/#{POLYLINE_ENDPOINT}"
    headers = {'content-type': 'application/json', 'x-api-key': TOLLGURU_API_KEY}
    body = {
      'source': "bing",
      'polyline': google_encoded_polyline,
      **request_parameters,
    }
    tollguru_response = HTTParty.post(tollguru_url,:body => body.to_json, :headers => headers, :timeout => 200)
    begin
        toll_body = JSON.parse(tollguru_response.body)
        if toll_body["route"]["hasTolls"] == true
            return google_encoded_polyline,toll_body["route"]["costs"]["tag"], toll_body["route"]["costs"]["cash"] 
        else
            raise "No tolls encountered in this route"
        end
    rescue Exception => e
        puts e.message 
    end
end
