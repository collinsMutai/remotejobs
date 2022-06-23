import os
from flask import Flask, redirect, render_template, request, abort, jsonify, session, url_for
from flask_cors import CORS


from models import setup_db, Jobs

import requests
import pathlib
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google.oauth2 import id_token

from auth import login_is_required, flow, GOOGLE_CLIENT_ID



def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = "Collo"
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    
    @app.route("/login")
    def login():
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)
  

    @app.route("/callback")
    def callback():
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500) #State does not match / cross-site forgery

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)
    

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        return redirect("/apply")




    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")


    @app.route("/")
    def index():
  
        return redirect(url_for("jobs"))

    @app.route("/jobs")
    def jobs():
        jobs = Jobs.query.all()

     
        

          
        return render_template("jobs.html", jobs=jobs)



    @app.route("/jobs/<job_id>")
    def job_detail(job_id):
        job = Jobs.query.filter_by(id=job_id).first_or_404()


        details = {
            "intro": "The company employs around 30 people in",
            "job_brief": "We are looking for a talented UX Designer to work remotely with a Swiss-based deep-tech company focusing on the autonomization of document extraction through machine learning.",
            "requirements": ["Proven work experience as a UI/UX Designer or similar role",
            "Portfolio of design projects",
            "Knowledge of wireframe tools (e.g. Wireframe.cc and InVision)"]


            
        }

        return render_template("job-detail.html", job=details)

    @app.route("/apply")
    @login_is_required
    def apply():
        if "name" not in session:
            return redirect(url_for("login"))
    

        return render_template("/apply.html",  name=session["name"])
        
        # return "Submit application <a href='/logout'><button>Logout<\button></a>"



    return app

    if __name__ == "__main__":
        app.run()


