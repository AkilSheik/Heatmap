from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import io
import folium
import time
import requests
import json
import datetime
import urllib.request
import time
import sys
from geopy.geocoders import Nominatim

            

class Ui_MainWindow(object):                                                        #besttime API      
    def setupUi(self, MainWindow):
        def query(): 
            text = self.lineEdit.text()                                             # Gets input text
            geolocator = Nominatim(user_agent="geoapiExercises")                    #Defines Geocoder object
            url = "https://besttime.app/api/v1/venues/search"                       #Gets the data               
            
            requests.request("GET", url)                                             
            params = {
            'api_key_private': 'pri_0c8519fb761a474a8b30abd06f09ff23',
            'q': str(text),
            'num': 20,
            'fast': False
        }
            location = geolocator.geocode(text)
            response = requests.request("POST", url,  params=params)
            print(json.loads(response.text))



                    
            c1 = location.latitude                                                     #get longlat of search query
            c2 = location.longitude


                
            filter(c1,c2)                                                               #Passes the two coordinates to the filter function
                    
        def filter(cor1, cor2):                                                         #filter besttime data
            url = "https://besttime.app/api/v1/venues/filter" 
            params = {
                   'api_key_private': 'pri_0c8519fb761a474a8b30abd06f09ff23',
                   'busy_min': 0,
                   'lat': cor1,
                   'lng': cor2,
                   'radius': 20000

            }

            response = requests.request("GET", url, params=params)
            response = json.loads(response.text)
            print(response)

            display(response, cor1, cor2)

        def getHTMLCode(response, number):                                               #function for outputting API response into html for markers
            now = datetime.datetime.now()                                                #Used to get hour of day
            formatteddata = """                                                            
            <p style = "font-family: Arial">                                               
            <code>
            <h1>""" + str(response.get('venues')[number].get('venue_name'))  +  """</h1>""" + "\n"
            formatteddata = formatteddata + "Weather: " + str(weather(response.get('venues')[number].get('venue_lat'), response.get('venues')[number].get('venue_lng'))) + " degrees <br>" +"\n"
            formatteddata = formatteddata + "Average Solar Power: " + str(solar(response.get('venues')[number].get('venue_lat'), response.get('venues')[number].get('venue_lng'))) + " dni/year" +  "<br>" +"\n" 
            formatteddata = formatteddata + "Crowd Level Percent: " + str(response.get('venues')[number].get('day_raw')[now.hour - 1]) + "<br>" +"\n"
            formatteddata = formatteddata + "Max Crowd Percent For Day: " + str(response.get('venues')[number].get('day_info').get('day_max')) + "<br>" +"\n"
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
            return formatteddata                                                          #Returns HTML String


        def display(response1, cord1, cord2):
            m = folium.Map(location=[cord1, cord2], tiles = "Stamen Terrain", zoom_start=13)         #This modifies the map when you click the search bar, cord1 and cord2 represent the longitude and latitude
            now = datetime.datetime.now()                                                            
            for n in range(0,len(response1.get('venues')) - 1):                                      #for loops for displaying markers in map
                if(n > 20):
                    break
                iframe = folium.IFrame(html = getHTMLCode(response1, n), width=475, height=350)
                popup = folium.Popup(iframe, max_width=2000)
                maximum = response1.get('venues')[n].get('day_raw')[now.hour - 1]
                if(maximum < 20):                                                                     #elifs for determining intensity of buisness, which determines color (yellow is least busy, red is most busy)
                    color = '#FFEC19'  
                elif(maximum < 40):
                    color = "#FFC100"
                elif(maximum < 60):
                    color = '#FF9800'
                elif(maximum < 80):
                    color = '#FF5607'
                else:
                    color = '#F6412D'

                folium.CircleMarker(location = [response1.get('venues')[n].get('venue_lat'),response1.get('venues')[n].get('venue_lng')],  #markers
                                    radius = 2, color = color, popup = popup).add_to(m)
        
            data = io.BytesIO()                                                                                                             #stores map
            m.save(data, close_file=False)                                                                                                  
            self.view.setHtml(data.getvalue().decode())                                                                                     #PyQt5 opens map


        def weather(latitude, longitude):                                                                                                   #weather API

            url = "https://api.openweathermap.org/data/2.5/forecast?"

            params = {
                'appid': '39c873996e9fb79c84b155bc1e9e737e',
                'lat': latitude,
                'lon': longitude,
                'units': 'imperial'
            }

            response = requests.request("POST", url, params=params)
            response = response.json()
            return response['list'][0]['main']['temp']

                
        def solar(latitude, longitude):                                                                                                       #solar API



            url = "https://developer.nrel.gov/api/solar/solar_resource/v1.json?"

            params = {
                'api_key': 'PCLvAJCjIwjdtlXv2ratKQ9VevjmR5BTo6VJf0P4',
                'lat': latitude,
                'lon': longitude
            }

            response = requests.request("GET", url, params=params)
            response = response.json()
            return response['outputs']['avg_dni']['annual']

                
        

                                                                                                                        #pyQt5 GUI (generated mostly from QT designer)


            
            
        MainWindow.setObjectName("Globepoints")
        #self.setWindowTitle("Globepoints")
        MainWindow.resize(644, 659)                                                                                     #size
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")                                                                         #splitter for two objects at once on the same line
        self.lineEdit = QtWidgets.QLineEdit(self.splitter)                                                              #entry box
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setText("Example: Livingston NJ Fast Food")                                                       #placeholder text
        self.lineEdit.setObjectName("lineEdit")
        self.submitButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        sizePolicy.setHeightForWidth(self.submitButton.sizePolicy().hasHeightForWidth())
        self.submitButton.setSizePolicy(sizePolicy)
        self.submitButton.setObjectName("submitButton")                                                                 #submit button
        self.submitButton.clicked.connect(query)                                                                        #Button click calls query function to get map and besttime API          
        self.verticalLayout_4.addWidget(self.splitter)                                                                  #adds splitter to GUI                                       
        self.view = QtWebEngineWidgets.QWebEngineView()                                                                 #map definition
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.verticalLayout_4.addWidget(self.view)                                                                      #adds map to GUI
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 644, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        m = folium.Map(                                                                                                 #folium map definition (original map at startup)
          location=[45.5236, -122.6750], tiles="Stamen Terrain", zoom_start=13 
        )

        data = io.BytesIO()                                                                                             #defines data to store map
        m.save(data, close_file=False)                                                                                  #map saves
        self.view.setHtml(data.getvalue().decode())                                                                     #map displayed


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Globepoints", "Globepoints"))                                             #window name
        self.submitButton.setText(_translate("MainWindow", "Submit"))

if __name__ == "__main__":                                                                                              #essentials for running and closing program
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

