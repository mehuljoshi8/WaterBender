import dash_bootstrap_components as dbc
import dash_html_components as html
from imgUpload import ImgUpload
import dash_core_components as dcc

class Components:
	def __init__(self):
		self.navbar = dbc.NavbarSimple(
			[dbc.NavItem(dbc.NavLink("Create Login", href="/dashboard/")),],
			brand="Smart Watering",
			brand_href="/dashboard",
			color="dark",
			dark=True,
			sticky="top",
			style={"margin-bottom": "10px"}
		)

		self.location_input = dbc.Row([
			dbc.Col(
				dbc.Input(id="Input", placeholder="Input an address", type="text"),	
				width=9,
			),
			dbc.Col(
				dbc.Button("Search",id="search_location_btn", color="warning", className="mr-1"),
				width=3,
			)],
			no_gutters=True, style={"margin-top": 20})

		self.imgUpload = ImgUpload()

		self.plantCard = [dbc.Card([
			dbc.CardImg(id="card-img", src="https://ichef.bbci.co.uk/news/976/cpsprodpb/10ECF/production/_107772396_treesmall.jpg", top=True),
			html.H6("Scientific Name: Epipremnum aureum", style={"font-size": "11px", "text-align": "center"}),
		], style={"margin-bottom": 20}), self.imgUpload.uploads, self.location_input, 
		html.P(id="output_da_input"), html.Div(id="render_map")
		]


		self.Graph = html.Div([
						dcc.Graph(id="live_graph",),
						dcc.Interval(
							id="live_graph_interval",
							interval = 3600000,
							n_intervals=0,
						),	
					])


		self.pi_control_on = html.Div(dbc.Button("Water On", color="primary", className="mr-1", id="pi_on"), id="water_on")
		self.pi_control_off = html.Div(dbc.Button("Water off", color="danger", className="mr-1", id="pi_off"), id="water_off") 



	



	

