#Importing modules
import json
import requests
import os 
import polyline as Poly


'''Fetching Polyline from Google'''

#API key for google map
token=os.environ.get('google_api')

#Source and Destination Coordinates
#source
source = 'Newark, NJ 07114, United States'
#Destination
destination = 'Flushing, NY 11367, United States'

#Query Google maps with Key and Source-Destination coordinates
url = 'https://maps.googleapis.com/maps/api/directions/json?origin={a}&destination={b}&key={c}'.format(a=source,b=destination,c=token)

#converting the response to json
response=requests.get(url).json()

'''TODO #checking for errors in response '''


segments=response['routes'][0]['legs'][0]['steps']
coordinate_list=[]
for i in segments:
    coordinate_list.extend(Poly.decode(i['polyline']['points']))
polyline_from_google=Poly.encode(coordinate_list)



'''Calling Tollguru API'''

#API key for Tollguru
Tolls_Key = os.environ.get('tollguru_api')

#Tollguru querry url
Tolls_URL = 'https://dev.tollguru.com/v1/calc/route'

#Tollguru resquest parameters
headers = {
            'Content-type': 'application/json',
            'x-api-key': Tolls_Key
          }
params = {
            'source': "google",
            'polyline': polyline_from_google ,               
            'vehicleType': '2AxlesAuto',                #'''TODO - Need to users list of acceptable values for vehicle type'''
            'departure_time' : "2021-01-05T09:46:08Z"   #'''TODO - Specify time formats'''
        }

#Requesting Tollguru with parameters
response_tollguru= requests.post(Tolls_URL, json=params, headers=headers).json()

#checking for errors or printing rates
if str(response_tollguru).find('message')==-1:
    print('\n The Rates Are ')
    #extracting rates from Tollguru response is no error
    print(*response_tollguru['summary']['rates'].items(),end="\n\n")
else:
    raise Exception(response_tollguru['message'])