# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 17:03:55 2018
flask app fiddle with SQLA - intro flask SQLA tutorial

@author: yehan
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
		SECRET_KEY='topsecretkey',
		SQLALCHEMY_DATABASE_URI='postgresql://hungy:1234qwer@localhost/food_db',
#		SQLALCHEMY_DATABASE_URI='postgresql://postgres:1234qwer@localhost/food_db',
		SQLALCHEMY_TRACK_MODIFICATIONS=False,
		SQLALCHEMY_ECHO=True  # print debug to server log
	)
db = SQLAlchemy(app)  #db holds all the classes of SQLAlchemy
#db.init_app(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String)

	def __repr__(self):
		return 'ID: {0} User: {1} email: {2}'.format(self.id, self.username,
		    self.email)


class Recipe(db.Model):
	# __tablename__ = 'app.recipes'  # not how postgres schemas work
	__tablename__ = 'recipes'
	id = db.Column(db.Integer, primary_key=True)
	rec_name = db.Column(db.String, unique=True, nullable=False)


class Ingredient(db.Model):
	__tablename__ = 'ingredients'
	id = db.Column(db.Integer, primary_key=True)
	ing_name = db.Column(db.String, unique=True, nullable=False)


class XRecIng(db.Model):
	__tablename__ = 'x_rec_ing'
	id = db.Column(db.Integer, primary_key=True)
	rec_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
	ing_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
	qty = db.Column(db.Numeric)

db.create_all()
''' If you need to get the attached engine & binds for some reason
db.get_engine()
db.get_binds()
'''
# %% initial test data
user1 = User(username='hungy', email='hy@test.com', password='blah')

# add new recipe (check if already exists)
new_rec_name = 'porridge'
new_rec = Recipe(rec_name=new_rec_name)

# list of new ingredients
ing_names = ['water', 'rice', 'pork']

# add new ingredeints (TODO: check if already exists, only add if it doesn't)
# needs to return the ID for each ingredient
new_ing_list = [Ingredient(ing_name=ing) for ing in ing_names]

# %% session: Add to transaction, then run query to get the IDs to put into the
# x table
db.session.add(user1)
db.session.add(new_rec)
db.session.add_all(new_ing_list)
db.session.new


# %%
# add recipe ingredient qty
# get the IDs for rec/ingredients, then attach qty next to them

q_ing_ids = db.session.query(Ingredient)  # this will return entire db of ingredients
q_ing_ids.one().ing_name

ing_ids = []
for ing in ing_names:
	q_ing_ids = db.session.query(Ingredient).filter(Ingredient.ing_name.like('%'+ing+'%'))  # get IDs
	ing_ids.append(q_ing_ids.one().id)

for result in ing_ids.all():
	print(result.id, result.ing_name)

ing_ids = db.session.query(Ingredient)


rec_ing_qty = [


]



















