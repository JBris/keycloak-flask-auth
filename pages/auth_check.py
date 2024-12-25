import dash
from dash import callback, no_update, Input, Output, State, dcc
import dash_html_components as html

from datetime import datetime
import requests
from flask import redirect, session, redirect
import pytz
from datetime import datetime, timedelta

grant_type="password"
client_id="keycloak-jwt"
client_secret="pYAfGSs4Qanh8ISKS8LJ0dbNPt9JluZj"

def authenticate_user_pw(user: str, password: str):
    params = dict(
        username=user,
        password=password,
        grant_type=grant_type,
        client_id=client_id,
        client_secret=client_secret
    )

    resp = requests.post(
        "http://localhost:8080/realms/master/protocol/openid-connect/token",
        data=params
    )
    if resp.status_code != 200:
        return None

    token = resp.json()
    token["expires_in"] = datetime.now().replace(tzinfo=pytz.UTC) + timedelta(seconds = token["expires_in"] - 1)
    token["refresh_expires_in"] = datetime.now().replace(tzinfo=pytz.UTC) + timedelta(seconds = token["refresh_expires_in"] - 1)
    session["token"] = token

    return token

def authenticate_refresh_token(refresh_token: str):
    params = dict(
        refresh_token=refresh_token,
        grant_type=grant_type,
        client_id=client_id,
        client_secret=client_secret
    )

    resp = requests.post(
        "http://localhost:8080/realms/master/protocol/openid-connect/token",
        data=params
    )
    if resp.status_code != 200:
        return None

    token = resp.json()
    token["expires_in"] = datetime.now().replace(tzinfo=pytz.UTC) + timedelta(seconds = token["expires_in"] - 1)
    token["refresh_expires_in"] = datetime.now().replace(tzinfo=pytz.UTC) + timedelta(seconds = token["refresh_expires_in"] - 1)
    session["token"] = token

    return token

def has_valid_token():
    token = session.get("token")
    if token is None:
        return False
    
    now = datetime.now().replace(tzinfo=pytz.UTC)
    if now > token["refresh_expires_in"]:
        return False

    if now > token["expires_in"]:
        res = authenticate_refresh_token(token["refresh_token"])
        if res is None:
            return False
    
    return True