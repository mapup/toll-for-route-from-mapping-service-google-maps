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
    Tolls_URL = 'https://apis.tollguru.com/toll/v2/complete-polyline-from-mapping-service'
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
    

'''Testing'''
#Importing Functions
from csv import reader,writer
import time
temp_list=[]
with open('testCases.csv','r') as f:
    csv_reader=reader(f)
    for count,i in enumerate(csv_reader):
        #if count>2:
        #  break
        if count==0:
            i.extend(("Input_polyline","Tollguru_Tag_Cost","Tollguru_Cash_Cost","Tollguru_QueryTime_In_Sec"))
        else:
            try:
                polyline=get_polyline_from_google_maps(i[1],i[2])
                i.append(polyline)
            except:
                i.append("Routing Error") 
            
            start=time.time()
            try:
                rates=get_rates_from_tollguru(polyline)
            except:
                i.append(False)
            time_taken=(time.time()-start)
            if rates=={}:
                i.append((None,None))
            else:
                try:
                    tag=rates['tag']
                except:
                    tag=None
                try:
                    cash=rates['cash']
                except :
                    cash=None
                i.extend((tag,cash))
            i.append(time_taken)
        #print(f"{len(i)}   {i}\n")
        temp_list.append(i)

with open('testCases_result.csv','w') as f:
    writer(f).writerows(temp_list)

'''Testing Ends'''
