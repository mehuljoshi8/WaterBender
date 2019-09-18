import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc


app = dash.Dash(
	external_stylesheets=[dbc.themes.BOOTSTRAP],
)


app.layout = html.Div(
    [
        dbc.Button(
            "Open collapse",
            id="collapse-button",
            className="mb-3",
            color="primary",
        ),
        dbc.Collapse(
            html.H6("Hello world", style={"text-align": "center"}),
            id="collapse",
        ),

        html.Div(
    	[
	        dbc.Progress(id="progress", value=0, striped=True, animated=True),
	        dcc.Interval(id="interval", interval=250, n_intervals=0),
    	]
	)
    ]
)

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(Output("progress", "value"), [Input("interval", "n_intervals")])
def advance_progress(n):
	if(n < 100):
		return min(n % 110, 100)


if __name__ == "__main__":
	app.run_server()