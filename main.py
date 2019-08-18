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
import json
from components import Components
#Ending imports

#starting varibles
server = flask.Flask(__name__)
app = dash.Dash(
	__name__,
	server=server,
	external_stylesheets=[dbc.themes.BOOTSTRAP],
	routes_pathname_prefix="/dashboard/",
	# suppress_callback_exceptions=True
)

comp = Components()
data = {'time':[], 'temperature':[]}
latLng = {}
prev_data = {}
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
				comp.plantCard,
			),
			width=3,
			style={"padding-top": "10px"},
		),
		dbc.Col(
			html.Div(
				[
					dcc.Graph(
						id="live_graph",
					),
					dcc.Interval(
						id="live_graph_interval",
						interval = 60000,
						n_intervals=0,
					),	
				]),
			width=9,
		),
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
    Output("render_map", "children"),
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
		return html.Img(src=geolocation_dict['img_url'])
	else:
		return "Please enter a valid address"

#callback for the weatherman data
@app.callback(Output("live_graph", "figure"),
				[Input('live_graph_interval', 'n_intervals')]
)
def updateGraph(_):
	global prev_data, data
	print("in update graph")
	print(latLng)
	if latLng != {} and prev_data != latLng:
		lat, lng = latLng['lat'], latLng['lng']
		weatherman = WeatherManager(lat, lng)
		weatherman_data = eval(weatherman.__str__())
		data = weatherman_data['data']
		print(data)
		prev_data = {'lat': weatherman_data['lat'], 'lng': weatherman_data['lng']}
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['time'], y=data['temperature'], fill='tozeroy'))
	return fig

if __name__ == "__main__":
	app.run_server(debug=False)





