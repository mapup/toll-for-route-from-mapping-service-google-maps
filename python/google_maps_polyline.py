#Importing modules
import json
import requests
import os 
import polyline as poly

#API key for google map
token=os.environ.get('GOOGLE_API')
#API key for Tollguru
Tolls_Key = os.environ.get('Tollguru_API_New')


'''Fetching Polyline from Google'''
def get_polyline_from_google_maps(source,destination):
    #Query Google maps with Key and Source-Destination coordinates
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin={a}&destination={b}&key={c}'.format(a=source,b=destination,c=token)
    #converting the response to json
    response=requests.get(url).json()
    #extracting segments of the routes
    segments=response['routes'][0]['legs'][0]['steps']
    #temp_list to store all coordinates
    coordinate_list=[]
    for i in segments:
        coordinate_list.extend(poly.decode(i['polyline']['points']))
    polyline_from_google=poly.encode(coordinate_list)
    return(polyline_from_google)

        
        
'''Calling Tollguru API'''
def get_rates_from_tollguru(polyline):
    #Tollguru querry url
    Tolls_URL = 'https://dev.tollguru.com/v1/calc/route'
    #Tollguru resquest parameters
    headers = {
                'Content-type': 'application/json',
                'x-api-key': Tolls_Key
                }
    params = {
                #Explore https://tollguru.com/developers/docs/ to get best of all the parameter that tollguru has to offer 
                'source': "google",
                'polyline': polyline,                      # this is the encoded polyline that we made     
                'vehicleType': '2AxlesAuto',                #'''Visit https://tollguru.com/developers/docs/#vehicle-types to know more options'''
                'departure_time' : "2021-01-05T09:46:08Z"   #'''Visit https://en.wikipedia.org/wiki/Unix_time to know the time format'''
                }
    #Requesting Tollguru with parameters
    response_tollguru= requests.post(Tolls_URL, json=params, headers=headers,timeout=200).json()
    #print(response_tollguru)
    #checking for errors or printing rates
    if str(response_tollguru).find('message')==-1:
        return(response_tollguru['route']['costs'])
    else:
        raise Exception(response_tollguru['message'])
    

'''Program Starts'''
#Step 1 :Provide Source and Destination
#Source
source = '1100 E Spring Creek Pkwy, Plano, TX 75074, United States'              
#Destination
destination = '901 S Kobayashi Rd S, Webster, TX 77598, United States'

#Step 2 : Get Polyline from Arcgis
polyline_from_google=get_polyline_from_google_maps(source, destination)

#Step 3 : Get rates from Tollguru
rates_from_tollguru=get_rates_from_tollguru(polyline_from_google)

#Print the rates of all the available modes of payment
if rates_from_tollguru=={}:
    print("The route doesn't have tolls")
else:
    print(f"The rates are \n {rates_from_tollguru}")