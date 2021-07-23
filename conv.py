import folium
import folium
import requests
import json
import datetime

now = datetime.datetime.now()


m = folium.Map(location=[40.1911072, -74.4302871], zoom_start=8)

url = "https://besttime.app/api/v1/venues/search"
requests.request("GET", url)



params = {
    'api_key_private': 'pri_c59735d1c70f440385d894f88d92f509',
    'q': 'Mcdonalds in New Jersey',
    'num': 20,
    'fast': False
}



response = requests.request("POST", url, params=params)

url = "https://besttime.app/api/v1/venues/filter"

params = {
    'api_key_private': 'pri_c59735d1c70f440385d894f88d92f509',
    'busy_min': 0,
    'lat': 40.2331206,
    'lng': -74.684165,
    'radius': 2000000 
}



response = requests.request("GET", url, params=params)
response = json.loads(response.text)

for n in range(0,19):
        maximum = response.get('venues')[n].get('day_raw')[now.hour - 1]
        if(maximum < 20):
            color = '#FFEC19'
        elif(maximum < 40):
            color = "#FFC100"
        elif(maximum < 60):
            color = '#FF9800'
        elif(maximum < 80):
            color = '#FF5607'
        else:
            color = '#F6412D'
        print(maximum)
        print(color)
        folium.CircleMarker(location = [response.get('venues')[n].get('venue_lat'),response.get('venues')[n].get('venue_lng')], radius = 2, color = color).add_to(m)
        


    
m.save("heatmap.html")

