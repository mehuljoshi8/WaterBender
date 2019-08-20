# Creator: Mehul Joshi
# Geolocation.py gets an address and returns a packet of data that contains the lat, lng, img
import requests


#the geolocation manager has many fields but they are all private because the client program main.py
#should not be able to alter the fields inside geolocation
class GeolocationManager:
	def __init__(self, address):
		if address != None and address != "":
			print("Address passed:", address)
			self.__address = address
			self.__getGeoCodeData()

	def __str__(self):
		return str({'address':self.__address, 'lat': self.__lat, 'lng': self.__lng, 'img_url': self.__img_url})

	def __getGeoCodeData(self):
		print(self.__address)
		geolocation_key = KEY
		geolocation_url = "http://www.mapquestapi.com/geocoding/v1/address?key=" + geolocation_key + "&location=" + self.__address
		r = requests.get(geolocation_url)
		dict = r.json()
		latitude_longitude = dict['results'][0]['locations'][0]['latLng']
		self.__lat, self.__lng = latitude_longitude['lat'], latitude_longitude['lng']
		self.__img_url = dict['results'][0]['locations'][0]['mapUrl']





