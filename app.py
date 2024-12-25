import dash
import dash_html_components as html
import flask
from flask import redirect, session, redirect
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from datetime import datetime
import pytz
from dash import dcc, html 

server = flask.Flask(__name__)
server.secret_key = '!secret'

load_figure_template("MINTY")
app = dash.Dash(
    server=server, 
    external_stylesheets=[dbc.themes.MINTY],
    title="Keycloak Authentication",
    use_pages=True
)

app.layout = html.Div([
    dcc.Location(id="url",  refresh="callback-nav"),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=True)