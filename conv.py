import folium
import requests
import json
import datetime
import urllib.request
import time
import Tkinter as tk
from Tkinter import ttk
from PIL import Image, ImageTk
from Tkinter import *
import sys


now = datetime.datetime.now()




def query(textline):
        url = "https://besttime.app/api/v1/venues/search"
        requests.request("GET", url)
        params = {
        'api_key_private': 'pri_c59735d1c70f440385d894f88d92f509',
        'q': str(textline),
        'num': 20,
        'fast': False
}

        response = requests.request("POST", url,  params=params)
        link = json.loads(response.text).get('_links').get('venue_search_progress')
        with urllib.request.urlopen(link) as url:
                s = json.loads(url.read())
                print(s)
                time.sleep(5)
                c1 = s.get("bounding_box").get('lat')
                c2 = s.get("bounding_box").get('lng')
                filter(c1,c2)


def filter(cor1, cor2):
        url = "https://besttime.app/api/v1/venues/filter"
        params = {
           'api_key_private': 'pri_c59735d1c70f440385d894f88d92f509',
           'busy_min': 0,
           'lat': cor1,
           'lng': cor2,
           'radius': 20000

        }
        print(params)
        response = requests.request("GET", url, params=params)
        response = json.loads(response.text)
        print(response)
        display(response, cor1, cor2)



#print(response)

#print(response.get('venues')[0])
def getHTMLCode(response, number):
       formatteddata = """
       <p>
       <code>
       <h1>""" + str(response.get('venues')[number].get('venue_name'))  +  """</h1>""" + "\n"
       formatteddata = formatteddata + "Crowd Level Percent: " + str(response.get('venues')[number].get('day_raw')[now.hour - 1]) + "<br>" +"\n"
       formatteddata = formatteddata + "Max Crowd Percent: " + str(response.get('venues')[number].get('day_info').get('day_max')) + "<br>" +"\n"
       formatteddata = formatteddata + "Ratings: " + str(response.get('venues')[number].get('rating')) + "<br>" +"\n"
       formatteddata = formatteddata + "Reviews: " + str(response.get('venues')[number].get('reviews')) + "<br>" +"\n"
       formatteddata = formatteddata + "Adress: " + str(response.get('venues')[number].get('venue_address')) + "<br>" +"\n"
       formatteddata = formatteddata + "Maximum Dwell Time: " +str( response.get('venues')[number].get('venue_dwell_time_max')) + "<br>" +"\n"
       formatteddata = formatteddata + "Minimum Dwell Time: " + str(response.get('venues')[number].get('venue_dwell_time_min')) + "<br>" +"\n"
       formatteddata = formatteddata + "Type: " + str(response.get('venues')[number].get('venue_type')) + "<br>" +"\n"

       formatteddata = formatteddata +  """
       </code>
       </p>
        """
       return formatteddata


def display(response1, cord1, cord2):
        m = folium.Map(location=[cord1, cord2], zoom_start=8)

        for n in range(0,19):
                iframe = folium.IFrame(html = getHTMLCode(response1, n), width=475, height=350)
                popup = folium.Popup(iframe, max_width=2000)
                maximum = response1.get('venues')[n].get('day_raw')[now.hour - 1]
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
                #print(maximum)
                #print(color)
                folium.CircleMarker(location = [response1.get('venues')[n].get('venue_lat'),response1.get('venues')[n].get('venue_lng')],
                                    radius = 2, color = color, popup = popup).add_to(m)
                m.save("heatmap.html")




    
small_font = ('Verdana',1)
root = tk.Tk()



root.title("GlobePoints")
root.geometry("800x600")
style = ttk.Style(root)
root.tk.call('source', 'azure.tcl')
ttk.Style().theme_use('azure')                                                  #azure light theme


Grid.rowconfigure(root, 0, weight=1)                                             #text box larger than submit button
Grid.columnconfigure(root, 0, weight=3)
Grid.columnconfigure(root, 1, weight=1)
Grid.rowconfigure(root, 1, weight=100)                                           #map greater importance/size

query = tk.StringVar()
query_entry = ttk.Entry(root,textvariable = query, font=('calibre',18,'normal'))    #text box

enter = ttk.Button(root, text ="Submit", command= query(str(query_entry)))                            #submit button
query_entry.insert(0, 'place')
query_entry.grid(row=0,column=0, padx=30,pady=30, sticky="nsew")
enter.grid(row=0,column=1, pady=30, padx=20, sticky="nsew")


root.mainloop()


        






