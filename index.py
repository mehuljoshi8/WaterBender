import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import dashapp
import callbacks


if __name__ == "__main__":
	dashapp.app.run_server(debug=False)