import requests
import json


def weather(latitude, longitude):



    url = "https://api.openweathermap.org/data/2.5/forecast?"

    params = {
        'appid': '39c873996e9fb79c84b155bc1e9e737e',
        'lat': latitude,
        'lon': longitude,
        'units': 'imperial'
    }

    response = requests.request("POST", url, params=params)
    response = response.json()
    # print(json.dumps(response, indent=4))
    print(response['list'][0]['main']['temp'])

weather(40.730610, -73.935242)