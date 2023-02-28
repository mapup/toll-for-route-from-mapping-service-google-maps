# toll-google-maps
Calculate tolls for routes (polylines) from Google maps

Click on the folders above to see examples to extend mapping capabilities of Google by adding toll information from [**TollGuru**](https://tollguru.com/) to the route information from Google.

The toll information has following [key features](https://tollguru.com/developers/features):
### Support for [geographies](https://github.com/mapup/tollguru_country_coverage/wiki/Countries-supported-by-TollGuru) 
* North America - Bahamas, Belize, Canada, Costa Rica, Cuba, Dominican Republic, Guatemala, Honduras, Jamaica, Mexico, Panama, Puerto Rico, United States of America
* Europe - Albania, Andorra, Austria, Belarus, Belgium, Bosnia and Herzegovina, Bulgaria, Croatia, Czechia, Denmark, Estonia, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Latvia, Lithuania, Luxembourg, Moldova, Montenegro, Netherlands, North Macedonia, Norway, Poland, Portugal, Romania, Russia, Serbia, Slovakia, Slovenia, Spain, Sweden, Switzerland, Turkey, United Kingdom
* Australia - Australia, New Zealand
* Asia - Brunei, India, Indonesia, Malaysia, Philippines, Singapore, Taiwan, Thailand, Vietnam
* Latin America - Argentina, Bolivia, Brazil, Chile, Colombia, Ecuador, Guyana, Paraguay, Peru, Uruguay, Venezuela

### Based on vehicles in use in each country, [vehicle type support](https://github.com/mapup/tollguru_vehicle_coverage/wiki/Vehicle-types-supported-by-TollGuru)
* Car, SUV or Pickup truck. You can specify number of axles including axles in trailers
* Carpool
* Taxi
* Rideshare
* Motorcycle
* Truck
* Bus
* Recreational vehicle (RV), motorhome, caravan, van

### Rates for all the available payment options in local currencies
* Tag transponder (including primary and secondary transponders)
* cash
* licence plate
* credit card
* prepaid

### Time based tolls
You can specify "departure_time" as DateTime (string) or Timestamp (number) to provide you with most accurate toll rates based on time of day/week/month/year, including tolls for express lanes where tolls change as quickly as every five minutes

### All types of toll systems
Support for barrier, ticket system and distance based tolling configurations

### Support for [all map services](https://github.com/mapup)
[See the Mapping services list](https://github.com/mapup/toll-google-maps/wiki/2.-Map-platform-service-supported-by-TollGuru) for all mapping platforms supported. You can edit the **source** argument to send polyline from another mapping service.

### Support for trucks based on [height, weight, harardous goods, etc.](https://github.com/mapup/toll-google-maps/wiki/4.-Truck-parameters-supported-by-TollGuru)
You can receive tolls based on vehicle height, weight etc., while calculating toll: "truckType","shippedHazardousGoods","tunnelCategory","truckRestrictionPenalty" and [more](https://github.com/mapup/toll-google-maps/wiki/4.-Truck-parameters-supported-by-TollGuru).








