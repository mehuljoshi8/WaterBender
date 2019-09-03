# Creator: Mehul Joshi
# This handles the main interaction between the geolocation, latlng encoding, display preferences, and pi manipulation

#Starting Imports
import flask
from dash.dependencies import Input, Output, State
from dashapp import DashApp
import art
#Ending imports
dashapp = DashApp()

# #call back for in the input value
@dashapp.app.callback(Output("output_da_input", "children"), [Input("Input", "value")])
def output_text(value):
	return dashapp.output_text(value)

#call back for the time that shows the current time
@dashapp.app.callback(Output("live_time_updates", 'children'),
                [Input('time_interval', "n_intervals")])
def update_time(n):
   return dashapp.update_time(n)
#call back for the map url and geolocation data
@dashapp.app.callback(
    [Output("render_map", "children"), Output("grapher", "children")],
    [Input('search_location_btn', 'n_clicks')],
    state=[State(component_id="Input", component_property="value")]
)
def update_map_img(_, address):
	return dashapp.update_map_img(_, address)

#callback for the weatherman data
@dashapp.app.callback(Output("live_graph", "figure"),
				[Input('live_graph_interval', 'interval'), Input("grapher-tabs", "active_tab")]
)
def updateGraph(n, active_tab):
	return dashapp.updateGraph(n, active_tab)
#callback to update the data for weatherman
@dashapp.app.callback(Output("random_div", "children"), [Input("live_graph_interval", "interval")])
def updateData(n):
	art.tprint("Updating data","rnd-xlarge")
	dashapp.updateData(n)
	return ""
#plant recognition
@dashapp.app.callback([Output('card-img', 'src'),Output('plant_data', "children")], [Input('upload-image', 'contents')])
def updateImg(contents):
	art.tprint("Updating Image","rnd-na")
	return dashapp.updateImg(contents)

#alter this code once you get the pi back working
@dashapp.app.callback(Output("water_cont", "children"), [Input('pi', "n_clicks")])
def toggleWater(_):
	# return dashapp.toggleWater(_)
	return "hello"
#alteration for pi code ends here


if __name__ == "__main__":
	dashapp.app.run_server(debug=False)





