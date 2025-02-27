import time
import fileinput
import requests as req
from tkinter import *
from tkinter import ttk
import json

def getApiId():
    a = fileinput.input('api-key.txt')
    b = []
    for i in a:
        b.append(i)
    
    c = b[0]
    d = c.strip()
    return d

api_key = getApiId()

geocodeURL = 'http://api.openweathermap.org/geo/1.0/direct?q={cityname}&limit={limit}&appid={apikey}'

currentWeatherURL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units=metric'

entryValue = ""

class city():
    def __init__(self, name, lat, lon, country):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country

def getCityData(cityName: str):
    res = req.get(geocodeURL.format(cityname = cityName, limit = 5, apikey = api_key))
    a = res.json()
    if a.__len__() <= 0:
        print("cant find city")
        return None

    b = a[0]
    #print(b)
    #jsonData = json.loads(b)
    jsonData = b
    #print(jsonData)
    cityData = city(name = jsonData['name'], lat = jsonData['lat'], lon = jsonData['lon'], country = jsonData['country'])

    return cityData
    #print(cityData.lat)
    #exit()

def getWeatherData(cityData: city):
    if cityData == None:
        print("no city data recived")
        return None

    res = req.get(currentWeatherURL.format(lat = cityData.lat, lon = cityData.lon, apikey = api_key))
    a = res.json()
    #print(a)
    b = a['weather']
    wdat = b[0]
    main = a['main']
    visibility = a['visibility']
    summary = wdat['main']
    description = wdat['description']
    temp = main['temp']
    minTemp = main['temp_min']
    maxTemp = main['temp_max']
    feelsLike = main['feels_like']
    pressure = main['pressure']
    humidity = main['humidity']
    wind = a['wind']
    windSpeed = wind['speed']
    windDir = wind['deg']
    data = [cityData.name, cityData.country, summary, description, temp, minTemp, maxTemp, feelsLike, pressure, humidity, visibility, windSpeed, windDir]
    #b = []
    #print(data)
    return data

def citySubmit():
    entryValue = cityTextBox.get()
    #print('\n', entryValue, '\n')
    reRender(getWeatherData(getCityData(entryValue.strip())))

hasDoneOneQuery = False
underContainer = None
ucRight = None
ucLeft = None
cityLabels = []
weatherLabels = []

def reRender(data):
    if data == None or data.__len__() <= 0:
        return None

    global hasDoneOneQuery
    global underContainer
    global ucLeft
    global ucRight
    global cityLabels
    global weatherLabels

    if not hasDoneOneQuery:
        underContainer = ttk.Frame(main)
        underContainer.grid(column=10, row=31)
        ucLeft = ttk.Frame(underContainer)
        ucRight = ttk.Frame(underContainer)
        ucLeft.grid(column=11, row=40)
        ucRight.grid(column=20, row=40)

        cl1 = ttk.Label(ucLeft, text="CityData")
        cl2 = ttk.Label(ucLeft, text="Name")
        cl3 = ttk.Label(ucLeft, text="Country")
        cl4 = ttk.Label(ucLeft, text="Summary")
        cl5 = ttk.Label(ucLeft, text="Description")
        cl6 = ttk.Label(ucLeft, text="Temperature")
        cl7 = ttk.Label(ucLeft, text="MinTemp")
        cl8 = ttk.Label(ucLeft, text="MaxTemp")
        cl9 = ttk.Label(ucLeft, text="FeelsLike")
        cl10 = ttk.Label(ucLeft, text="Pressure")
        cl11 = ttk.Label(ucLeft, text="Humidity")
        cl12 = ttk.Label(ucLeft, text="Visibility")
        cl13 = ttk.Label(ucLeft, text="WindSpeed")
        cl14 = ttk.Label(ucLeft, text="WindDirection")

        wl1 = ttk.Label(ucRight, text="WeatherData")
        wl2 = ttk.Label(ucRight)
        wl3 = ttk.Label(ucRight)
        wl4 = ttk.Label(ucRight)
        wl5 = ttk.Label(ucRight)
        wl6 = ttk.Label(ucRight)
        wl7 = ttk.Label(ucRight)
        wl8 = ttk.Label(ucRight)
        wl9 = ttk.Label(ucRight)
        wl10 = ttk.Label(ucRight)
        wl11 = ttk.Label(ucRight)
        wl12 = ttk.Label(ucRight)
        wl13 = ttk.Label(ucRight)
        wl14 = ttk.Label(ucRight)

        cityLabels = [cl1, cl2, cl3, cl4, cl5, cl6, cl7, cl8, cl9, cl10, cl11, cl12, cl13, cl14]
        weatherLabels = [wl1, wl2, wl3, wl4, wl5, wl6, wl7, wl8, wl9, wl10, wl11, wl12, wl13, wl14]

        for i in cityLabels:
            i.grid()
        
        for i in weatherLabels:
            i.grid()

        hasDoneOneQuery = True

    for i in range(1, data.__len__() + 1):
        weatherLabels[i]['text'] = str(data[i-1])


    



    

root = Tk()
topContainer = ttk.Frame(root, height=600, width=800)
topContainer.grid()
main = ttk.Frame(topContainer, relief="raised", borderwidth=5, padding=20)
main.grid(column=10, row=9)
title = ttk.Label(main, text="python weather app")
title.grid(column=10, row=10)
cityTextBox = ttk.Entry(main)
cityTextBox.grid(column=10, row=20)
submitButton = ttk.Button(main, text="submit", command=citySubmit)
submitButton.grid(column=10, row=30)
root.title("weather-app")

root.mainloop()