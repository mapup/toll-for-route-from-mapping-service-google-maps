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
