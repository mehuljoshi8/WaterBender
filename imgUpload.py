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

    def parse_contents(contents):
        html.Img(src=contents),

# import datetime

# import dash
# from dash.dependencies import Input, Output, State
# import dash_core_components as dcc
# import dash_html_components as html

# # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__)
# app.layout = html.Div([
#     dcc.Upload(
#         id='upload-image',
#         children=html.Div([
#             'Upload an ',
#             html.A('image', style={"color": "#007FFF", 'text-decoration':'underline'})
#         ]),
#         style={
#             'width': '100%',
#             'height': '60px',
#             'lineHeight': '60px',
#             'borderWidth': '1px',
#             'borderStyle': 'solid',
#             'borderRadius': '5px',
#             'textAlign': 'center',
#             'margin': '10px',
#         },
#         # Allow multiple files to be uploaded
#         multiple=True
#     ),
#     html.Div(id='output-image-upload'),
# ])





# @app.callback(Output('output-image-upload', 'children'),
#               [Input('upload-image', 'contents')],
#               [State('upload-image', 'filename'),
#                State('upload-image', 'last_modified')])
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n, d) for c, n, d in
#             zip(list_of_contents, list_of_names, list_of_dates)]
#         return children


# if __name__ == '__main__':
#     app.run_server(debug=True)