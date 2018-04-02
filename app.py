from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy  # this is a modified SQLAlchemy specific to flask
from sqlalchemy.dialects import postgresql as pg  # get postgres specific types

# Create Flask instance
app = Flask(__name__)
# 'binds' the database to the flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234qwer@localhost/food_db'  # target database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # print debug to server log
db = SQLAlchemy(app)

# %% DB connection testing
db.drop_all()
db.create_all()

#%% backend database model - definitions only
# DB class used to create the database table and interface with it
# New items are inserted as instances with the data in the correct variable

class Recipes(db.Model):
	__tablename__ = "recipes"  #also optional
	rec_id = db.Column(db.Integer, primary_key=True)
	rec_name = db.Column(db.String, nullable=False)  # note only Postgres/SQLite don't require length
	rec_author = db.Column(db.String)
	rec_active = db.Column(db.Boolean)
	ing_list = db.Column(pg.ARRAY(db.String, dimensions=1))

	# def __init__(self, rec_id, rec_name, rec_author, ing_list):
		# don't need __init__ method, it's auto - generated

	def __repr__(self):
		'''String here formatted to print about the instance in question'''
		return 'Recipe ID: {0} Name: {1}'.format(self.rec_id, self.rec_name)

class User(db.Model):
	"""Test example"""
	__tablename__ = "users"
	user_id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True)

	def __init__(self, email):
		'''The default constructor will use as many params as there are
		params in the class. We will override that has a consturctor
		which just calls a single param input'''
		self.email = email

	def __repr__(self):
		return 'E-mail: {0}'.format(self.email)


# %% Frontend template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/')
def hello():
    return 'Hello, World'

# this one has to be called via a url link on the html page
@app.route('/register', methods=['POST'])
def register():
	email = None
	if request.method == 'POST':
		email = request.form['email']
		# check email already exists
		if not db.session.query(User).filter(User.email == email).count():
			reg = User(email)
			# this calls the constructor for User and requires appropriate param inputs
			db.session.add(reg)
			# this INSERTS the data into the target table
			db.session.commit()
			return render_template('success.html')
	return render_template('index.html')


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == '__main__':
	app.debug = True
	app.run()