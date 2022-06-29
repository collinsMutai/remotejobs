import os
from flask import Flask, redirect, render_template, request, abort, jsonify, session, url_for
from flask_cors import CORS
import requests
import pathlib
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google.oauth2 import id_token

app = Flask(__name__)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

GOOGLE_CLIENT_ID = "391335116450-tt75nnq01kf04dlr3rcljbn00kqv318k.apps.googleusercontent.com"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile", 
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
        ],
    redirect_uri="http://127.0.0.1:5000/callback"        
    )

def login_is_required(function):
    def wrapper(*args,**kwargs):
        if "google_id" not in session:
            return abort(401) # Authorization required
        else:
            return function()
    return wrapper

