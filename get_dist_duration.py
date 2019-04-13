import requests
import json

def send_request(source, destination, api_key):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="+source+"&destinations="+destination+"&key="+api_key
    requests = session.get(url)

    return requests

def get_miles(r):
    test_json = json.loads(requests.text)['rows']
    return test_json[0]['elements'][0]['distance']['text']

def get_duration(r):
    test_json = json.loads(requests.text)['rows']
    return test_json[0]['elements'][0]['duration']['text']

src = "Portland, OR"
dst = "Seattle, WA"
api_key = "AIzaSyCrH8QL2z5GifRE7L8OI1slr-7a1Pexd9I"
session = requests.Session()
requests = send_request(src, dst, api_key)

print(get_miles(requests))
print(get_duration(requests))

