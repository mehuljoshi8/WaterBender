from app import dashapp
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user
from models import User
from forms import LoginForm
from werkzeug.urls import url_parse

@dashapp.server.route("/")
def index():
	if current_user.is_authenticated:
		return dashapp.app.index()
	return render_template('index.html')

@dashapp.server.route("/dashboard")
def dashboard():
	return dashapp.app.index()


@dashapp.server.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user == None:
			user = User.query.filter_by(email=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		print(form.remember_me.data)
		login_user(user, remember=form.remember_me.data)
		flash("Login requested")
		return redirect(url_for("index"))
	return render_template("login.html", form=form)


