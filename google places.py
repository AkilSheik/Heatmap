import requests
import json


def place(input):

    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"

    params = {
        'key': 'AIzaSyBuASUTc58ai6Ee1dmlxrt-bI8WKpWUX1o',
        'input': input,
        'inputtype': 'textquery',
        'fields': 'photos,formatted_address,name,rating,opening_hours,geometry,price_level'
    }

    response = requests.request("POST", url, params=params)
    response = response.json()
    print(json.dumps(response, indent=4))
    # print(response['candidates'][0]['formatted_address'])

place('Empire State Building')