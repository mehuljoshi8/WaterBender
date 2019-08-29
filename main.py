# Creator: Mehul Joshi
# This handles the main interaction between the geolocation, latlng encoding, display preferences, and pi manipulation

#Starting Imports
import flask
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from plotly import graph_objs as go
import datetime
import dash_html_components as html
from geolocationmanager import GeolocationManager
from weathermanager import WeatherManager
from components import Components
from pi import Pi_Control
from plantdatahandler import Recognizer
#Ending imports

#starting varibles
server = flask.Flask(__name__)
app = dash.Dash(
	__name__,
	server=server,
	external_stylesheets=[dbc.themes.BOOTSTRAP],
	routes_pathname_prefix="/dashboard/",
	suppress_callback_exceptions=True,
)

comp = Components()
# pi = Pi_Control()
data = {}
latLng = {}
prev_data = {}
default_plant_img = "https://ichef.bbci.co.uk/news/976/cpsprodpb/10ECF/production/_107772396_treesmall.jpg"
water_button_counter = 0

#ending variables

#basic layout for the dash app dashboard
app.layout = html.Div([
	comp.navbar,
	html.P(id="live_time_updates", style={"margin-left": "10px"}),
	dcc.Interval(
		id="time_interval",
		interval = 1000,
		n_intervals = 0
	),
	dbc.Row(
		[dbc.Col(
			html.Div(
				[comp.plantCard,
				comp.imgUpload.uploads,
				comp.location_input, 
				html.P(id="output_da_input"),
				html.Div(id="render_map")]
			),
			width=3,
			style={"padding-top": "10px"},
		),
		dbc.Col(id="grapher", width=9)
	])
])
#end of layout

#call back for in the input value
@app.callback(Output("output_da_input", "children"), [Input("Input", "value")])
def output_text(value):
	if value != None:
		return "Your Input: " + str(value)
	else:
		"What are you waiting for..."

#call back for the time that shows the current time
@app.callback(Output("live_time_updates", 'children'),
                [Input('time_interval', "n_intervals")])
def update_time(n):
    style = {
        "padding": "12px",
        "fontsize": "25px"
    }
    return html.Span(datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"), style=style)

#call back for the map url and geolocation data
@app.callback(
    [Output("render_map", "children"), Output("grapher", "children")],
    [Input('search_location_btn', 'n_clicks')],
    state=[State(component_id="Input", component_property="value")]
)
def update_map_img(_, address):
	global latLng, data, prev_data
	latLng = {}
	data = {'time':[], 'temperature':[]}
	prev_data = {}
	if address != None and address != "":
		geoman = GeolocationManager(address)
		geolocation_str = geoman.__str__()
		geolocation_dict = eval(geoman.__str__())
		latLng['lat'], latLng['lng'] = geolocation_dict['lat'], geolocation_dict['lng']
		return html.Img(src=geolocation_dict['img_url'], style={"width": "100%"}), comp.graph_output(address)
	else:
		return "Please enter a valid address", html.Div()

#callback for the weatherman data
@app.callback(Output("live_graph", "figure"),
				[Input('live_graph_interval', 'interval'), Input("grapher-tabs", "active_tab")]
)
def updateGraph(n, active_tab):
	print(n)
	active_tab= active_tab.split("-")[0]
	global prev_data, data
	lat, lng = latLng['lat'], latLng['lng']
	weatherman = WeatherManager(lat, lng)
	weatherman_data = eval(weatherman.__str__())
	data = weatherman_data['data']
	print(data)
	prev_data = {'lat': weatherman_data['lat'], 'lng': weatherman_data['lng']}
	layout= getLayout(active_tab)
	fig = go.Figure(layout=layout)
	fig.add_trace(go.Scatter(x=data['time'], y=data[active_tab], fill='tozeroy', name="Temperature"))
	return fig

def getLayout(var):
	return go.Layout(
		xaxis=dict(
			title= 'Time (Hours)'
		),
		yaxis=dict(
			title= var
		)
	)

@app.callback(Output('card-img', 'src'), [Input('upload-image', 'contents')])
def updateImg(contents):
	if contents == None or not contents[0][0:10] == "data:image": 
		return default_plant_img

	plantRecognizer = Recognizer(contents)
	request_id = plantRecognizer.identify()
	print(request_id)
	suggestions = plantRecognizer.get_suggestions(request_id)
	print(suggestions)
	for suggestion in suggestions:
		print(suggestion['plant']['name'], suggestion['id'], suggestion['probability'], suggestion['confidence'])
	return contents

#alter this code once you get the pi back working
@app.callback(Output("water_cont", "children"), [Input('pi', "n_clicks")])
def toggleWater(_):
	global water_button_counter
	if water_button_counter % 2 == 0:
		water_button_counter += 1
		# Code to turn raspberry pi off with the solenoid config
		pi.off()
		return dbc.Button("Water On", color="primary", className="mr-1", id="pi")
	water_button_counter += 1
	#Code to turn the water counter on with the soleniod config
	pi.on()
	return dbc.Button("Water Off", color="danger", className="mr-1", id="pi")
#alteration for pi code ends here


if __name__ == "__main__":
	app.run_server(debug=False)
