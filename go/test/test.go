package main

import (
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

var TOLLGURU_API_KEY string = os.Getenv("TOLLGURU_API_KEY")
var GMAPS_API_KEY string = os.Getenv("GMAPS_API_KEY")

const (
	GMAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"

	TOLLGURU_API_URL  = "https://apis.tollguru.com/toll/v2"
	POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service"
)

var (
	source      string
	destination string
)

// Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
var requestParams = map[string]interface{}{
	"vehicle": map[string]interface{}{
		"type": "2AxlesAuto",
	},
	// Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
	"departure_time": "2021-01-05T09:46:08Z",
}

type Polyline struct {
	Points string `json:"points"`
}

type LatLng struct {
	Lat float64 `json:"lat"`
	Lng float64 `json:"lng"`
	// The latitude in degrees. It must be in the range [-90.0, +90.0].
}

func readCsvFile(filePath string) [][]string {
	// Open the file
	csvfile, err := os.Open(filePath)
	if err != nil {
		log.Fatalln("Couldn't open the csv file", err)
	}

	// Parse the file
	r := csv.NewReader(csvfile)
	records, err := r.ReadAll()
	if err != nil {
		log.Fatal("Unable to parse file as CSV for ", err)
	}

	return records

}

type AutoGenerated struct {
	Routes []struct {
		Legs []struct {
			Steps []struct {
				Polyline struct {
					Points string `json:"points"`
				} `json:"polyline"`
			}
		}
	}
}

func main() {
	records := readCsvFile("test.csv")
	for i := 1; i < len(records); i++ {
		source = records[i][1]
		destination = records[i][2]

		url := fmt.Sprintf("%s?origin=%s&destination=%s&key=%s", GMAPS_API_URL, source, destination, GMAPS_API_KEY)

		spaceClient := http.Client{
			Timeout: time.Second * 60, // Timeout after 60 seconds
		}

		req, err := http.NewRequest(http.MethodGet, url, nil)
		if err != nil {
			log.Fatal(err)
		}

		req.Header.Set("User-Agent", "spacecount-tutorial")

		res, getErr := spaceClient.Do(req)
		if getErr != nil {
			log.Fatal(getErr)
		}

		if res.Body != nil {
			defer res.Body.Close()
		}

		body, readErr := ioutil.ReadAll(res.Body)
		if readErr != nil {
			log.Fatal(readErr)
		}
		var polyline AutoGenerated

		jsonErr := json.Unmarshal(body, &polyline)
		if jsonErr != nil {
			log.Fatal(polyline)
		}

		points := make([]string, len(polyline.Routes[0].Legs[0].Steps))
		polyline_decoded := make([][]LatLng, len(polyline.Routes[0].Legs[0].Steps))
		polyline_encoded := []LatLng{}

		for i := range polyline.Routes[0].Legs[0].Steps {
			points[i] = polyline.Routes[0].Legs[0].Steps[i].Polyline.Points
			polyline_decoded[i] = DecodePolyline(points[i])

			polyline_encoded = append(polyline_encoded, DecodePolyline(points[i])...)
		}

		polyline_final := Encode(polyline_encoded)

		// Tollguru API request

		url_tollguru := fmt.Sprintf("%s/%s", TOLLGURU_API_URL, POLYLINE_ENDPOINT)

		params := map[string]interface{}{
			"source":   "google",
			"polyline": polyline_final,
		}

		for k, v := range requestParams {
			params[k] = v
		}

		requestBody, err := json.Marshal(params)

		request, err := http.NewRequest("POST", url_tollguru, bytes.NewBuffer(requestBody))
		request.Header.Set("x-api-key", TOLLGURU_API_KEY)
		request.Header.Set("Content-Type", "application/json")

		client := &http.Client{
			Timeout: time.Second * 60,
		}
		resp_toll, err := client.Do(request)
		if err != nil {
			panic(err)
		}
		defer resp_toll.Body.Close()

		body_toll, error := ioutil.ReadAll(resp_toll.Body)
		if error != nil {
			log.Fatal(err)
		}

		var cost map[string]interface{}
		jsonEr := json.Unmarshal([]byte(body_toll), &cost)
		if jsonEr != nil {
			log.Fatal(cost)
		}

		toll := cost["route"].(map[string]interface{})["costs"].(map[string]interface{})["tag"]
		fmt.Printf("The toll rate for source%s and destination %s is%v:\n", toll, source, destination)

	}
}
func DecodePolyline(poly string) []LatLng {
	p := &Polyline{
		Points: poly,
	}
	return p.Decode()
}

// Decode converts this encoded Polyline to an array of LatLng objects.
func (p *Polyline) Decode() []LatLng {
	input := bytes.NewBufferString(p.Points)

	var lat, lng int64
	path := make([]LatLng, 0, len(p.Points)/2)
	for {
		dlat, _ := decodeInt(input)
		dlng, err := decodeInt(input)
		if err == io.EOF {
			return path
		}

		lat, lng = lat+dlat, lng+dlng
		path = append(path, LatLng{
			Lat: float64(lat) * 1e-5,
			Lng: float64(lng) * 1e-5,
		})
	}
}

// Encode returns a new encoded Polyline from the given path.
func Encode(path []LatLng) string {
	var prevLat, prevLng int64

	out := new(bytes.Buffer)
	out.Grow(len(path) * 4)

	for _, point := range path {
		lat := int64(point.Lat * 1e5)
		lng := int64(point.Lng * 1e5)

		encodeInt(lat-prevLat, out)
		encodeInt(lng-prevLng, out)

		prevLat, prevLng = lat, lng
	}

	return out.String()
}

// decodeInt reads an encoded int64 from the passed io.ByteReader.
func decodeInt(r io.ByteReader) (int64, error) {
	result := int64(0)
	var shift uint8

	for {
		raw, err := r.ReadByte()
		if err != nil {
			return 0, err
		}

		b := raw - 63
		result += int64(b&0x1f) << shift
		shift += 5

		if b < 0x20 {
			bit := result & 1
			result >>= 1
			if bit != 0 {
				result = ^result
			}
			return result, nil
		}
	}
}

// encodeInt writes an encoded int64 to the passed io.ByteWriter.
func encodeInt(v int64, w io.ByteWriter) {
	if v < 0 {
		v = ^(v << 1)
	} else {
		v <<= 1
	}
	for v >= 0x20 {
		w.WriteByte((0x20 | (byte(v) & 0x1f)) + 63)
		v >>= 5
	}
	w.WriteByte(byte(v) + 63)
}
