# Creator: Mehul Joshi
# imgUpload handles the state where the user wants to change which plant they uploaded

import datetime
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
class ImgUpload:
    def __init__(self):
        self.uploads = dcc.Upload(
            
            dbc.Button("Upload Image", color="primary", className="mr-1"),
            id="upload-image",
            style={
                "text-align": 'center'
            }
        )