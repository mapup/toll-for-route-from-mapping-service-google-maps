#Importing modules
import json
import requests
import os 
import polyline as poly
'''Fetching Polyline from Google'''
#API key for google map
token=os.environ.get('google_api')
#Source and Destination Coordinates
#source
source = '251 West, IN-120, Fremont, IN 46737'
#Destination
destination = '2323 Willowcreek Rd, Portage, IN 46368'
#Query Google maps with Key and Source-Destination coordinates
url = 'https://maps.googleapis.com/maps/api/directions/json?origin={a}&destination={b}&key={c}'.format(a=source,b=destination,c=token)
#converting the response to json
response=requests.get(url).json()
print(response)
'''TODO #checking for errors in response '''
segments=response['routes'][0]['legs'][0]['steps']
coordinate_list=[]
for i in segments:
    coordinate_list.extend(poly.decode(i['polyline']['points']))
polyline_from_google=poly.encode(coordinate_list)
#print(polyline_from_google)


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
response_tollguru= requests.post(Tolls_URL, json=params, headers=headers,timeout=500).json()
#checking for errors or printing rates
if str(response_tollguru).find('message')==-1:
    print('\n The Rates Are ')
    #extracting rates from Tollguru response is no error
    print(*response_tollguru['route']['costs'].items(),end="\n\n")
else:
    raise Exception(response_tollguru['message'])