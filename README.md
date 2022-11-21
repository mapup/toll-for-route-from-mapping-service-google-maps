# toll-google-maps
Click on the folders above to see examples to extend mapping capabilities of Google by adding toll information from [**TollGuru**](https://tollguru.com/) to the route information from Google.

The toll information has following [key features](https://tollguru.com/developers/features):
### Support for [geographies](https://github.com/mapup/tollguru_country_coverage/wiki/Countries-supported-by-TollGuru) 
* North America - Bahamas, Belize, Costa Rica, Cuba, Dominican Republic, El Salvador, Guatemala, Honduras, Jamaica, Nicaragua, Panama, Puerto Rico, United States of America
* Europe - Albania, Andorra, Austria, Belarus, Belgium, Bosnia and Herzegovina, Bulgaria, Croatia, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Kosovo, Latvia, Liechtenstein, Lithuania, Luxembourg, Malta, Moldova, Monaco, Montenegro, Netherlands, North Macedonia, Norway, Poland, Portugal, Romania, Russia, San Marino, Serbia, Slovakia, Slovenia, Spain, Sweden, Switzerland, Turkey, Ukraine, United Kingdom
* Australia - Australia, New Zealand
* Asia - Bangladesh, India, Indonesia, Laos, Malaysia, Myanmar, Philipines, Singapore, Taiwan, Thailand, Vietnam
* Latin America - Argentina, Bolivia, Brazil, Chile, Colombia, Ecuador, Falkland Islands, French Guiana, Guyana, Paraguay, Peru, Suriname, Uruguay, Venezuela

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








