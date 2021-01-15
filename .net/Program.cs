using System;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Net;
using System.IO;
using RestSharp;
namespace Google_Maps
{
    class Program
    {
        static void Main(string[] args)
        {
            string api_key="Api_Key";
            string source = "Dallas, TX";
            string destination = "New York, NY";
            string url = "https://maps.googleapis.com/maps/api/directions/json?origin="+source+"&destination="+destination+"&key="+api_key;
            
            WebRequest request = WebRequest.Create(url);
            WebResponse response = request.GetResponse();
            string responseFromServer;
            using (Stream dataStream = response.GetResponseStream())
            {
                // Open the stream using a StreamReader for easy access.
                StreamReader reader = new StreamReader(dataStream);
                // Read the content.
                responseFromServer = reader.ReadToEnd();
                
            }
            response.Close();
            //Parsing the respone into Json Format
            dynamic json  = JsonConvert.DeserializeObject(responseFromServer);
            //Cutting the json only for polyline's object
            json = json.routes[0].legs[0].steps;
            //Console.WriteLine(data);
            string polyline="";
            foreach(var value in json){
                //concatination  small pieces of polyline into the whole
                polyline = polyline + value.polyline.points;
            }

/** Implementing TollGuru Toll API **/

        var client = new RestClient("https://dev.tollguru.com/v1/calc/route");
        var request_tollguru = new RestRequest(Method.POST);
        request_tollguru.AddHeader("content-type", "application/json");
        request_tollguru.AddHeader("x-api-key", "your-api-key");
        request_tollguru.AddParameter("application/json", "{\"source\":\"google\" , \"polyline\":\""+polyline+"\" }", ParameterType.RequestBody);
        //Executing the request
        IRestResponse response1 = client.Execute(request_tollguru);        
        //Storing the data in content variable
        var content = response1.Content;
        Console.WriteLine(content);
        //Split and cutting the reponse
        string[] result = content.Split("tag\":");
        string[] temp1 = result[1].Split(",");
        string cost = temp1[0];
        Console.WriteLine(cost);
        }
    }
}


