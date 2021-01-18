# API Testing
* We have written few source and destination locations all over the world so that Toll rates from the API can be verified

### Note:
* Toll Rates can change for a particular from-to location. This is mainly due to two reasons
* Variable time tolls (tolls vary from time. Peak hours can have high rates)
* Different route polyline from google due to traffic congestion or road closure

### Test Files Usage
* TestCase output file has the route polyline and UTC query time included for a given source and target.
* Tag rates and cash rates which ever is applicable is given for 2AxlesAuto
* If any discrepancy is encountered in toll rates, polyline can be verified with the given one.


```ruby
require 'csv'
require_relative 'helper_ruby'

rows = Array.new
CSV.foreach('testCases.csv') do |row|
    rows << row
end

#Created a helper module to call the API for different source and destination combinations
rows[1..].each_with_index do |val,index|
    begin
        puts index+1
        poly,tag_cost,cash_cost = get_toll_rate(val[1],val[2])
        rows[index+1][4],rows[index+1][5],rows[index+1][6] = poly,tag_cost,cash_cost
        rows[index+1][7] = Time.now.utc.strftime("%T")
    rescue Exception => e
        puts e.message
        next
    end
end

#Writes the rates and polylines to a csv
File.write("testCases_output.csv", rows.map(&:to_csv).join)
puts "File output is finished with #{rows.length()-1} cases updated"

```