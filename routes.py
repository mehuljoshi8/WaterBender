from app import dashapp, db
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from models import User
from forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse

@dashapp.server.route("/")
def index():
	if current_user.is_authenticated:
		dashapp.update_layout(current_user)
		return redirect(url_for("dashboard"))
	return render_template('index.html')

@dashapp.server.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not user:
			user = User.query.filter_by(email=form.username.data).first()
		if not user or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))

		login_user(user, remember=form.remember_me.data)
		current_user.active = True
		db.session.commit()
		flash("Successfully logined in for " + current_user.username)
		return redirect(url_for("index"))
	return render_template("login.html", form=form)

@dashapp.server.route("/logout")
def logout():
	current_user.active = False
	db.session.commit()
	logout_user()
	flash("Successfully Logged out...")
	return redirect(url_for('index'))

@dashapp.server.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not user:
			user = User.query.filter_by(email=form.email.data).first()
		if not user:
			user = User(form.username.data,form.email.data, form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('Created a user for ' + form.username.data)
			return redirect(url_for('login'))
		flash("Sorry those credentials are already in the database")	
		#filter by username and email. If both of return none then create a user in the database
		#and autologin
	return render_template("register.html", form=form)

@dashapp.server.route("/dashboard")
def dashboard():
	if current_user.is_authenticated:
		return render_template("dashboard.html", username=current_user.username)
	flash("Please login to view your custom dashboard")
	return redirect(url_for("index"))

@dashapp.server.errorhandler(401)
def invalid_credentials(error):
	return "You are a stupid ugly m***** f*****!!"