import dash
from dash import callback, no_update, Input, Output, State, dcc
import dash_html_components as html

from datetime import datetime
import requests
from flask import redirect, session, redirect
import pytz
from datetime import datetime, timedelta

dash.register_page(__name__)

from .auth_check import authenticate_user_pw, authenticate_refresh_token

@callback(
    Output("url", "href"),
    Input('login-bttn', 'n_clicks'),
    State("user-input", "value"),
    State("password-input", "value"),
    prevent_initial_call=True
)
def login(n_clicks: int, user: str, password: str):
    if n_clicks is None:
        return no_update
    
    if user is None or password is None:
        return no_update

    res = authenticate_user_pw(user, password)
    if res is None:
        return redirect("/", code=302)
    
    return "/"


layout = [
    dcc.Loading([
        dcc.Input(
            id="user-input",
            type="text",
            placeholder="Enter username",
        ),
        dcc.Input(
            id="password-input",
            type="password",
            placeholder="Enter password",
        ),
        html.Button('Login', id='login-bttn'),
        html.Div(id='login-results'),
    ],
    id = 'page-loading')
]
