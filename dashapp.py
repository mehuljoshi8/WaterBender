#Creator: Mehul Joshi
#This is a version of main.py that is more object oriented so that it performs better
#Starting Imports
from flask import Flask
from flask_login import login_required
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from plotly import graph_objs as go
import datetime
import dash_html_components as html
from geolocationmanager import GeolocationManager
from weathermanager import WeatherManager
from components import Components
from pi import Pi_Control
from plantdatahandler import Recognizer
import time
import pandas as pd
import plotly.express as px
#Ending imports


class DashApp:
	def __init__(self):
		self.server = Flask(__name__)
		self.app = dash.Dash(
			name="dashboard",
			server=self.server,
			external_stylesheets=[dbc.themes.BOOTSTRAP],
			routes_pathname_prefix="/dashboard/",
			suppress_callback_exceptions=True,
		)

		#makes sure that the login is required for data vis
		for view_func in self.server.view_functions:
			if view_func.startswith("/dashboard/"):
				print(view_func)
				self.server.view_functions[view_func] = login_required(self.server.view_functions[view_func])

		self.comp = Components()
		# self.pi = Pi_Control()
		self.data = {}
		self.latLng = {}
		self.prev_data = {}
		self.default_plant_img = "https://ichef.bbci.co.uk/news/976/cpsprodpb/10ECF/production/_107772396_treesmall.jpg"
		self.water_button_counter = 0
		self.suggestions = None
		#ending variables

		#basic layout for the dash app dashboard
		self.app.layout = html.Div([
			self.comp.navbar,
		])
		#end of layout

#call back for in the input value
	def output_text(self, value):
		if value != None:
			return "Your Input: " + str(value)
		else:
			"What are you waiting for..."

	#Funtion that displays the current date and time
	def update_time(self, n):
	    style = {
	        "padding": "12px",
	        "fontsize": "25px"
	    }
	    return html.Span(datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"), style=style)

	#Funtion that updates the map url when an address is entered
	def update_map_img(self, _, address):
		self.latLng = {}
		self.data = {'time':[], 'temperature':[]}
		self.prev_data = {}
		if address != None and address != "":
			geoman = GeolocationManager(address)
			geolocation_str = geoman.__str__()
			print(geolocation_str)
			geolocation_dict = eval(geoman.__str__())
			self.latLng['lat'], self.latLng['lng'] = geolocation_dict['lat'], geolocation_dict['lng']
			return (html.Img(src=geolocation_dict['img_url'], style={"width": "100%"}), self.comp.graph_output(address))
		else:
			return "Please enter a valid address", html.Div()

	#Funtion to update the graph based on the active tab and the n_interval
	def updateGraph(self, n, active_tab):
		print(n)
		active_tab= active_tab.split("-")[0]
		lat, lng = self.latLng['lat'], self.latLng['lng']
		print(self.data)
		time.sleep(1)
		df = pd.DataFrame.from_dict(self.data, orient="index")
		df = df.transpose()
		fig = px.area(df, x='time', y=active_tab, template="plotly_white")
		return fig

	def updateData(self, n):
		weatherman = WeatherManager(self.latLng['lat'], self.latLng['lng'])
		weatherman_data = eval(weatherman.__str__())
		self.data = weatherman_data['data']

	#Uses cutting edge computer vision research to classify plants and give suggestions based on a picture of that plant
	def updateImg(self, contents):
		print("in update image")
		if contents == None or not contents[0:10] == "data:image":
			card = self.comp.initializePlantCard(self.default_plant_img, [])
			print(card)
			return card
		self.plantRecognizer = Recognizer(contents)
		request_id = self.plantRecognizer.identify()
		suggestions = self.plantRecognizer.get_suggestions(request_id)
		suggestions = [elem for elem in suggestions if not elem['plant']['common_name'] == ""]
		print(suggestions)
		self.suggestions = suggestions
		return self.comp.initializePlantCard(contents, 
				html.Div([html.H6(suggestions[0]['plant']['common_name'], id="plant_name", style={"text-align": "center", "font-size": "13px"}),
						dbc.Button("Confirm", id="confirm", color="success", className="mr-1", style={"width": "30%"}),
						dbc.Button("Reject", id="reject", color="danger", className="mr-1", style={"width": "30%"}),], style={"text-align": "center"}
				))

	#Confirms the suggestion and returns the name of the plant
	def confirmSuggestion(self):
		print(self.suggestions[0]['id'])
		self.plantRecognizer.confirm_suggestion(self.suggestions[0]['id'])
		print("Thank you for confirming my suggestion")
		return html.H6(self.suggestions[0]['plant']['common_name'], id="plant_name", style={"text-align": "center", "font-size": 13})

	def rejectSuggestion(self):
		print("Ok we are rejecting the suggestion")
		print(self.suggestions[0]['id'])
		self.plantRecognizer.reject_suggestion(self.suggestions[0]['id'])
		if len(self.suggestions) > 1:
			self.suggestions.pop(0)
			print(self.suggestions)
			return html.Div([html.H6(self.suggestions[0]['plant']['common_name'], id="plant_name", style={"text-align": "center", "font-size": "13px"}),
						dbc.Button("Confirm", id="confirm", color="success", className="mr-1", style={"width": "30%"}),
						dbc.Button("Reject", id="reject", color="danger", className="mr-1", style={"width": "30%"}),], style={"text-align": "center"})
		if len(self.suggestions) == 1:
			self.suggestions.pop(0)
			print("Suggestions length == 1", self.suggestions)
			#return a div with an input field and a button to submit the plant name
			return dbc.Row([
			dbc.Col(
				dbc.Input(id="plant_input", placeholder="Plant Name", type="text"),	
				width=9,
			),
			dbc.Col(
				dbc.Button("Submit",id="submit_plant_name", color="dark", className="mr-1"),
				width=3,
			)],no_gutters=True, id="plant_stuff")
	#alter this code once you get the pi back working
	def toggleWater(self, _):
		if self.water_button_counter % 2 == 0:
			self.water_button_counter += 1
			# Code to turn raspberry pi off with the solenoid config
			self.pi.off()
			return dbc.Button("Water On", color="primary", className="mr-1", id="pi")
		self.water_button_counter += 1
		#Code to turn the water counter on with the soleniod config
		self.pi.on()
		return dbc.Button("Water Off", color="danger", className="mr-1", id="pi")
	#alteration for pi code ends here

	def update_layout(self, current_user):
		print(current_user.username)		
		WATER_BENDER_LOGO = "https://raw.githubusercontent.com/csmjoshi/WaterBender/master/waterbender.png"
		ef = dbc.ButtonGroup(
			[
				dbc.DropdownMenu(
					[dbc.DropdownMenuItem("Add Community", href="/add_community", external_link=True), dbc.DropdownMenuItem("Add Plant", href="/add_plant", external_link=True)],
					group=True,
					right=True,
					label="+",
					in_navbar=True,
					color="primary",
				),
				dbc.DropdownMenu(
					[dbc.DropdownMenuItem("My Profile", href="/my_profile", external_link=True), dbc.DropdownMenuItem("My Communities", href="/my_communities", external_link=True), dbc.DropdownMenuItem("My Plants", href="/my_plants", external_link=True), dbc.DropdownMenuItem("Sign Out", href="/logout", external_link=True)],
					group=True,
					right=True,
					label=current_user.username,
					in_navbar=True,
					color="primary"
				),
			],
			className="ml-auto flex-nowrap mt-3 mt-md-0"
		)


		navbar = dbc.Navbar(
		    [
		        html.A(
		            dbc.Row(
		                [
		                    dbc.Col(html.Img(src=WATER_BENDER_LOGO, height="30px")),
		                    dbc.Col(dbc.NavbarBrand("Water Bender", className="ml-2")),
		                ],
		                align="center",
		                no_gutters=True,
		            ),
		            href="/#",
		        ),
		        ef
		    ],
		    color="dark",
		    dark=True,
		)

		self.app.layout = html.Div([
			navbar,
			html.P(id="live_time_updates", style={"margin-left": "10px"}),
			dcc.Interval(
				id="time_interval",
				interval = 1000,
				n_intervals = 0
			),
			dbc.Row(
				[dbc.Col(
					html.Div(
						[self.comp.plantCard,
						self.comp.imgUpload.uploads,
						self.comp.location_input, 
						html.P(id="output_da_input"),
						html.Div(id="render_map")]
					),
					width=3,
					style={"padding-top": "10px"},
				),
				dbc.Col(id="grapher", width=9)
			]),

		])

		

