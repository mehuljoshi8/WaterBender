# Creator: Mehul Joshi
# Testing git push
# I want this file to handle all the flask stuff
from dashapp import DashApp
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


dashapp = DashApp()
dashapp.server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
dashapp.server.config["SECRET_KEY"] = "you-will-never-guess"
db = SQLAlchemy(dashapp.server)
Bootstrap(dashapp.server)
login = LoginManager(dashapp.server)
