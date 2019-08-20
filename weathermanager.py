# Creator: Mehul Joshi
# weathermanager.py handles all of the processes that go in to displaying the graphs.
import requests
import time

class WeatherManager:
	def __init__(self, lat, lng):
		self.__lat = lat
		self.__lng = lng
		self.__getWeatherData()

	#returns the lat, lng, and data in a dictionary
	def __str__(self):
		return str({"lat":self.__lat, "lng":self.__lng, "data":self.__data})

	#sets the weather data
	#here is an update that I would suggest
	#first get the data for the time at the time of creating the object then get the data hourly for the rest of the time
	#also figure out how to store the data in a db so that even if the page reloads the user can still keep track of the temp
	def __getWeatherData(self):
		API_KEY = Key
		weather_url = "https://api.darksky.net/forecast/" + str(API_KEY) + "/" + str(self.__lat) + "," + str(self.__lng)
		r = requests.get(weather_url)
		dict = r.json()
		self.__data = {}
		counter = 24
		for entry in dict['hourly']['data']:
			if counter >= 0:
				for k in entry.keys():
					#convert unix time to 24 hour time
					if k == "time":
						time_str = time.strftime("%D %H:%M", time.localtime(int(entry[k])))
						entry[k] = time_str
					#appends the value if it is not in the dict
					if k not in self.__data.keys():
						self.__data[k] = [entry[k]]
					elif entry[k] not in self.__data[k]:
						self.__data[k].append(entry[k])
			counter = counter - 1
				





