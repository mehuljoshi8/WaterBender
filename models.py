from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	img_url = db.Column(db.String(20), nullable=False, default="default.jpg")
	password = db.Column(db.String(60), nullable=False)
	#define a one to many relationship here to the community

	def __repr(self):
		return f"User({self.username})','{self.email}','{self.img_url}','{self.password}"

class Community(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False, default=f"Community {self.id}")
	pi_zero_ip_address = db.Column(db.String(40), nullable=False)
	#Define a one to many relationship here to the plants

	def __repr(self):
		return f"Community({self.name}','{self.pi_zero_ip_address})"

class Plant(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	img_url = db.Column(db.String(20), nullable=False)



