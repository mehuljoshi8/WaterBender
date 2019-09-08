# Creator: Mehul Joshi
# I want this file to handle all the flask stuff
from dashapp import DashApp
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_bootstrap import Bootstrap

dashapp = DashApp()
dashapp.server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(dashapp.server)
Bootstrap(dashapp.server)
@dashapp.server.route("/")
def index():
	return render_template('index.html')

@dashapp.server.route("/dashboard/")
def dashboard():
	return dashapp.app.index()

