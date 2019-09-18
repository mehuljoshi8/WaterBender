#Creator: Mehul Joshi
#This file is fine as it stands no mods needed other than getting away from plant.id
import requests
from time import sleep
import base64


class Recognizer:
	def __init__(self, img_url):
		self.__img_url = [img_url]
		self.__secret_key = "7AV6KXYQSsIFRpA3pIDShtcINAWsFsFLdmnbPSkbYZm2nwoaw1"
		self.__headers = {
			'Content-Type': 'application/json'
		}
		
	def identify(self):
		print("Sending the image for identification")
		params = {
			'latitude': 49.194161,
			'longitude': 16.603017,
			'week': 23,
			'images': self.__img_url,
			'key': self.__secret_key,
			'parameters': ["crops_fast"]
		}

		response = requests.post('https://api.plant.id/identify', json=params, headers=self.__headers)
		print(response.status_code)
		if response.status_code != 200:
			print(response.text)
			raise("send_for_identificattion error: {}".format(response.text))

		return response.json().get('id')


	def get_suggestions(self, request_id):
		print("Waiting for suggestions...")
		params = {
	    	"key": self.__secret_key,
	    	"ids": [request_id]
		}
		while True:
			res = requests.post('https://plant.id/api/check_identifications', json=params, headers=self.__headers).json()
			if res[0]["suggestions"]:
				self.suggestions = res[0]['suggestions']
				return res[0]["suggestions"]


	def confirm_suggestion(self, suggestion_id):
		print("Confirming Suggestion...")
		params = {
			"key": self.__secret_key,
		}

		headers = {
			"Content-Type": "application/text"
		}
		res = requests.post("https://plant.id/api/confirm/{}".format(suggestion_id), json=params, headers=headers)
		print(res)

	def reject_suggestion(self, suggestion_id):
		print("Unconfirming suggesion...")
		params = {
			"key": self.__secret_key,
		}
		headers = {
			"Content-Type": "application/text",
		}

		res = requests.post("https://plant.id/api/unconfirm/{}".format(suggestion_id), json=params, headers=headers)
		print(res)

	def get_usage_info(self):
		params = {
			"key": self.__secret_key
		}
		response = requests.post('https://api.plant.id/usage_info', json=params, headers=self.__headers)
		print(response.status_code)
		return response.json()



		


