import time
import fileinput
import requests as req
from tkinter import *
from tkinter import ttk
import json

def getApiId():
    a = fileinput.input('ignore/api-key.txt')
    b = []
    for i in a:
        b.append(i)
    
    c = b[0]
    d = c.strip()
    return d

api_key = getApiId()

geocodeURL = 'http://api.openweathermap.org/geo/1.0/direct?q={cityname}&limit={limit}&appid={apikey}'

currentWeatherURL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units=metric'

class city():
    def __init__(self, name, lat, lon, state, country):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.state = state
        self.country = country

def getCityData(cityName: str):
    res = req.get(geocodeURL.format(cityname = cityName, limit = 5, apikey = api_key))
    a = res.json()
    b = a[0]
    #print(b)
    #jsonData = json.loads(b)
    jsonData = b
    cityData = city(name = jsonData['name'], lat = jsonData['lat'], lon = jsonData['lon'], state = jsonData['state'], country = jsonData['country'])

    return cityData
    #print(cityData.lat)
    #exit()

def getWeatherData(cityData: city):
    res = req.get(currentWeatherURL.format(lat = cityData.lat, lon = cityData.lon, apikey = api_key))
    print(res.json())
    exit()

ct = input("enter city")
ct = ct.strip()
ct = ct.lower()

ctDat = getCityData(ct)
getWeatherData(ctDat)

time.sleep(1000)