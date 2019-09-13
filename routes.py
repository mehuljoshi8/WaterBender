from app import dashapp, db
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from models import User
from forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse

@dashapp.server.route("/")
def index():
	if current_user.is_authenticated:
		print("Im in index and the current user is:", current_user.username)
		dashapp.update_layout(current_user)
		return redirect("/dashboard")
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
		print(form.remember_me.data)
		login_user(user, remember=form.remember_me.data)
		flash("Login requested")
		return redirect(url_for("index"))
	return render_template("login.html", form=form)

@dashapp.server.route("/logout")
def logout():
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
			user = User(username=form.username.data, email=form.email.data)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('Created a user for' + form.username.data)
			return redirect(url_for('index'))
		flash("Sorry those credentials are already in the database")	
		#filter by username and email. If both of return none then create a user in the database
		#and autologin

	return render_template("register.html", form=form)


@dashapp.server.errorhandler(401)
def invalid_credentials(error):
	return "You are a stupid ugly m***** f*****!!"