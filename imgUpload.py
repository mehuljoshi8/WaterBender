# Creator: Mehul Joshi
# imgUpload handles the state where the user wants to change which plant they uploaded

import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

class ImgUpload:
    def __init__(self):
        self.uploads = dcc.Upload(
            id="upload-image",
            children=html.Div([
                "Upload an ",
                html.Span('image', style={"color": "#007bff", 'text-decoration':'underline'})
            ]),
            style={
                'width': '100%',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '5px',
                'text-align': 'center',

            },
            multiple=True
        )