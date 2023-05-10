require 'HTTParty'
require 'json'
require "fast_polylines"
require 'cgi'

def get_toll_rate(source_val,dest_val)
    # Source Details
    source = source_val
    # Destination Details
    destination = dest_val

    # GET Request to Google for Polyline Pieces
    key = ENV['GOOGLEAPI_KEY']
    google_url = "https://maps.googleapis.com/maps/api/directions/json?origin=#{CGI::escape(source)}&destination=#{CGI::escape(destination)}&key=#{key}"
    response = HTTParty.get(google_url)
    json_parsed = JSON.parse(response.body)

    # Decoding polyline pieces and encoding back after combining all pieces
    polyline_piece = json_parsed['routes'].map { |x| x['legs'] }.flatten.map { |y| y['steps']}.flatten.map { |z| z['polyline']['points']}
    coord_decoded = polyline_piece.map {|x| FastPolylines.decode(x)}.flatten(1)
    google_encoded_polyline = FastPolylines.encode(coord_decoded)

    # Sending POST request to TollGuru
    tollguru_url = 'https://apis.tollguru.com/toll/v2/complete-polyline-from-mapping-service'
    tollguru_key = ENV['TOLLGURU_KEY']
    headers = {'content-type' => 'application/json', 'x-api-key' => tollguru_key}
    body = {'source' => "google", 'polyline' => google_encoded_polyline, 'vehicleType' => "2AxlesAuto", 'departure_time' => "2020-07-02T05:31:06Z"}
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
