from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
	username = StringField("Email/Username", validators=[DataRequired()], render_kw={"placeholder": "Email/Username"})
	password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
	remember_me = BooleanField("Remember Me")
	submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Username"})
	email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "Email"})
	password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired()], render_kw={"placeholder": "Confirm Password"})
	submit = SubmitField("Sign Up")

