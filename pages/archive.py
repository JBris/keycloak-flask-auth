import dash
from dash import html
from .auth_check import has_valid_token

from dash import callback, no_update, Input, Output, State, dcc

dash.register_page(__name__)

@callback(
    Output('archive-div', 'children'),
    Input('archive-h', 'children'),
)
def auth_check(children: str):
    if has_valid_token():
        return no_update
    else:
        return dcc.Location(pathname="/login", id="dummy-archive")

layout = layout = dcc.Loading([
    html.Div([
        html.H1('This is our Archive page', id='archive-h'),
        html.Div('This is our Archive page content.', id='archive-div'),
    ])    
])