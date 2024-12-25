import dash
from dash import html
from .auth_check import has_valid_token

from dash import callback, no_update, Input, Output, State, dcc


dash.register_page(__name__, path='/')

@callback(
    Output('home-div', 'children'),
    Input('home-h', 'children'),
)
def auth_check(children: str):
    if has_valid_token():
        return no_update
    else:
        return dcc.Location(pathname="/login", id="dummy-home")

layout = dcc.Loading([
    html.Div([
        html.H1('This is our Home page', id='home-h'),
        html.Div('This is our Home page content.', id='home-div'),
    ])    
])