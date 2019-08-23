import dash_bootstrap_components as dbc
import dash_html_components as html
from imgUpload import ImgUpload
import dash_core_components as dcc

class Components:
	def __init__(self):
		self.navbar = self.__initializeNavBar()
		self.location_input = self.__initializeLocationInput()
		self.imgUpload = ImgUpload()
		self.plantCard = self.__initializePlantCard()
		self.graph = self.__initializeGrapher()
		self.pi_control_on = html.Div(dbc.Button("Water On", color="primary", className="mr-1", id="pi_on"), id="water_on")
		self.pi_control_off = html.Div(dbc.Button("Water off", color="danger", className="mr-1", id="pi_off"), id="water_off") 

	def __initializeNavBar(self):
		return dbc.NavbarSimple(
			[dbc.NavItem(dbc.NavLink("Create Login", href="/dashboard/")),],
			brand="Smart Watering",
			brand_href="/dashboard",
			color="dark",
			dark=True,
			sticky="top",
			style={"margin-bottom": "10px"}
		)

	def __initializeLocationInput(self):
		return dbc.Row([
			dbc.Col(
				dbc.Input(id="Input", placeholder="Input an address", type="text"),	
				width=9,
			),
			dbc.Col(
				dbc.Button("Search",id="search_location_btn", color="warning", className="mr-1"),
				width=3,
			)],
			no_gutters=True, style={"margin-top": 20})
	
	def __initializePlantCard(self):
		return [dbc.Card([
			dbc.CardImg(id="card-img", src="", top=True),
			html.H6("Scientific Name: Epipremnum aureum", style={"font-size": "11px", "text-align": "center"}),
		], style={"margin-bottom": 20}), self.imgUpload.uploads, self.location_input, 
		html.P(id="output_da_input"), html.Div(id="render_map")
		]

	def __initializeGrapher(self):
		return html.Div([
						dcc.Graph(id="live_graph",),
						dcc.Interval(
							id="live_graph_interval",
							interval = 3600000,
							n_intervals=0,
						),	
					])

	#returns a dbc.Tabs element with the id of grapher-tabs
	def initializeTabsFeatures(self):
		tabs_list = [dbc.Tab(label='temperature', tab_id='temperature-tab'), 
					dbc.Tab(label='apparentTemperature', tab_id='apparentTemperature-tab'), 
					dbc.Tab(label='dewPoint', tab_id='dewPoint-tab'), 
					dbc.Tab(label='humidity', tab_id='humidity-tab'), 
					dbc.Tab(label='pressure', tab_id='pressure-tab'), 
					dbc.Tab(label='windSpeed', tab_id='windSpeed-tab'), 
					dbc.Tab(label='windGust', tab_id='windGust-tab'), 
					dbc.Tab(label='windBearing', tab_id='windBearing-tab'), 
					dbc.Tab(label='cloudCover', tab_id='cloudCover-tab'), 
					dbc.Tab(label='ozone', tab_id='ozone-tab')]
		return dbc.Tabs(tabs_list, id="grapher-tabs", active_tab="temperature-tab")


