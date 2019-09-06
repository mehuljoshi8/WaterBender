# Creator: Mehul Joshi
# I want this file to handle all the flask stuff

from dashapp import DashApp

dashapp = DashApp()
@dashapp.server.route("/")
def helo():
	return "hello world"


@dashapp.server.route("/dashboard/")
def dashboard():
	return dashapp.app.index()

