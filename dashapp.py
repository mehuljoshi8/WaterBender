#Creator: Mehul Joshi
#This is a version of main.py that is more object oriented so that it performs better
#Starting Imports
import flask
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
#Ending imports

class DashApp:
	def __init__(self):
		self.server = flask.Flask(__name__)
		self.app = dash.Dash(
			__name__,
			server=self.server,
			external_stylesheets=[dbc.themes.BOOTSTRAP],
			routes_pathname_prefix="/dashboard/",
			suppress_callback_exceptions=True,
		)
		self.comp = Components()
		# self.pi = Pi_Control()
		self.data = {}
		self.latLng = {}
		self.prev_data = {}
		self.default_plant_img = "https://ichef.bbci.co.uk/news/976/cpsprodpb/10ECF/production/_107772396_treesmall.jpg"
		self.water_button_counter = 0
		#ending variables

		#basic layout for the dash app dashboard
		self.app.layout = html.Div([
			self.comp.navbar,
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
		fig = go.Figure(layout=self.__getLayout(active_tab))
		time.sleep(1)
		fig.add_trace(go.Scatter(x=self.data['time'], y=self.data[active_tab], fill='tozeroy', name="Temperature"))
		return fig
	#Helper funtion that gets the layout for the graph
	def __getLayout(self, var):
		return go.Layout(
			xaxis=dict(
				title= 'Time (Hours)'
			),
			yaxis=dict(
				title= var
			)
		)

	def updateData(self, n):
		weatherman = WeatherManager(self.latLng['lat'], self.latLng['lng'])
		weatherman_data = eval(weatherman.__str__())
		self.data = weatherman_data['data']

	#Uses cutting edge computer vision research to classify plants and give suggestions based on a picture of that plant
	def updateImg(self, contents):
		if contents == None or not contents[0][0:10] == "data:image": 
			return self.default_plant_img

		plantRecognizer = Recognizer(contents)
		request_id = plantRecognizer.identify()
		print(request_id)
		suggestions = plantRecognizer.get_suggestions(request_id)
		print(suggestions)
		for suggestion in suggestions:
			print(suggestion['plant']['name'], suggestion['id'], suggestion['probability'], suggestion['confidence'])
		return contents

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


