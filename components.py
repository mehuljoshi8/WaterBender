import dash_bootstrap_components as dbc
import dash_html_components as html
from imgUpload import ImgUpload
import dash_core_components as dcc
from flask_login import current_user


class Components:
	def __init__(self):
		self.navbar = self.__initializeNavBar()
		self.location_input = self.__initializeLocationInput()
		self.imgUpload = ImgUpload()
		self.plantCard = dbc.Card(self.initializePlantCard("", []), id="plant_card")
		self.graph = self.__initializeGrapher()
		self.water_control = html.Div(dbc.Button("Water On", color="primary", className="mr-1", id="pi"), 
								id="water_cont", style={"text-align": "center", "margin": "5%"}) 

	def __initializeNavBar(self):
		return dbc.Navbar([
			html.A(href="/#", children=[
			dbc.Row([
				
					dbc.Col(html.Img(src="https://raw.githubusercontent.com/csmjoshi/WaterBender/master/waterbender.png", height="30px")),
					dbc.Col(dbc.NavbarBrand("Water Bender", className="ml-2")),
			], 
			no_gutters=True,
			align="center",),])
			
		],
		color="dark",
		dark=True
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
	
	def initializePlantCard(self, contents, children):
		return [dbc.CardImg(id="card-img", src=contents, top=True),
				html.Div(
					children=children,
					id="plant_data",
				)]
		

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
	def TabsFeatures(self):
		tabs_list = [dbc.Tab(label='temperature', tab_id='temperature-tab'), 
					dbc.Tab(label='apparentTemperature', tab_id='apparentTemperature-tab'), 
					dbc.Tab(label='dewPoint', tab_id='dewPoint-tab'), 
					dbc.Tab(label='humidity', tab_id='humidity-tab'), 
					dbc.Tab(label='pressure', tab_id='pressure-tab'), 
					dbc.Tab(label='windSpeed', tab_id='windSpeed-tab'), 
					dbc.Tab(label='ozone', tab_id='ozone-tab')]
		return dbc.Tabs(tabs_list, id="grapher-tabs", active_tab="temperature-tab", style={"text-align": "center"})

	def graph_output(self, address):
		return [html.H6(address, style={"text-align": "center", "text-decoration":"underline"}),
					self.water_control,
						html.Div(id="tabs-features", children=self.TabsFeatures(), style={"text-align":"center"}),
						self.graph, html.Div(id="random_div")]


