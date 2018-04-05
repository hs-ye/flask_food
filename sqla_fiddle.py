# -*- coding: utf-8 -*-
''' SQL Alchemy fiddle
20180-03-24
following the tute here
http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
'''

# check we're in the right environment
# the two installed sqlalchemy have different versions
# so using the below we can tell which version we're in.
# but spyder
import sqlalchemy
sqlalchemy.__version__  # should be 1.2.4 for correct environment


# %% set up class/object to connect to database
from sqlalchemy import create_engine
engine = create_engine("postgresql://hungy:1234qwer@localhost/food_db", echo=True)

# the class that links python classes to SQL tables
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, ARRAY  # case sensitive

# %%
class Recipe(Base):
	# this says that each Recipe will be stored in a table called recipes in the db
	__tablename__ = 'recipes'
	# all Column objects will be replaced by special SQL interfaces upon constructions
	rec_id = Column(Integer, primary_key=True)
	rec_name = Column(String)
	rec_ing_list = Column(ARRAY(String))

	def __repr__(self):
		# this is just to print objects of this class to console for testing
		return "Name: {0}, ID: {1}, Recipe List: {2}".format(
				self.rec_name, self.rec_id, self.rec_ing_list)


# %% how to check existint table
from sqlalchemy import MetaData  # singleton behaviour, contains info on all defns
META_DATA = MetaData(bind=engine)  # set up metadata object to connect to SQL backend
META_DATA.reflect(bind=engine)  # gets the class defns from the actual SQL backend
META_DATA.tables['recipes']  # gets the table defn in the connected db
# won't show up, unless committed change that writes to the DB
# %% Recipes meatadata...exposes same object Base metadata for some reason
'''
# But limited specifically to the Recipe class, whereas BASE covers all classes
# So if you clear base this will also be cleared,
TO BE TESTED: if you clear this, base should still have other defns, if any
'''
''' # Code:
Recipe.metadata.tables['recipes']  # on a declared class, check the tables
Recipe.metadata.clear
Recipe.metadata.drop_all(engine)  # on a declared class, check the tables
'''
# %% Send a CREATE TABLE command via the metadata table
Base.metadata.tables
'''
Base.metadata.clear()  # deletes the definitions managed by the Base Metadata
'''
Base.metadata.create_all(engine)  # creates all tables the metadata is aware of
Base.metadata.drop_all(engine)  # drops all tables the metadata is aware of
# will ignore existing tables already in db, not covered/defined by the metadata


# %% Create an instance of Recipe class (i.e. add a single new recipe)

thai_porridge = Recipe(rec_name='thai porridge', rec_ing_list=[
			'rice', 'fish sauce', 'pork mince'])

# %% create session to talk to database using ORM
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)  # define a custom Class with an engine bound
# note that Session is a CLASS - hence capital case

# Alternative way to instantiate Session:
#Session = sessionmaker() # if you don't have an engine yet and connect it later
#Session.configure(bind=engine)  # use the configure method

session = Session()  # instantiate the custom class that connects to right engine

session.add(thai_porridge)  # add to the session queue of stuff to change
session.new  # check for new adds in session memory

# db is lazy evaluated: no commits/held in memory until needed
retrieved_recipe = session.query(Recipe).filter_by(
		rec_name='thai porridge').first()
retrieved_recipe  # check the first thing that's retrieved

thai_porridge.rec_name = 'new porridge'
session.dirty  # check for changes

retrieved_recipe is thai_porridge  # amazingly, the ID has been updated/matched
# won't work if you re-define thai porridge withouht ID
# it will make a second entry and give it a new ID

thai_porridge.rec_name = 'thai porridge'  # change name back

# note that nothing is written to DB yet, until commit() call is done
session.add_all([
		Recipe(rec_name='pepproni pizza', rec_ing_list=[
				'pizza base', 'cheese', 'tomato paste', 'pepperoni']),
		Recipe(rec_name='fried rice', rec_ing_list=[
				'rice', 'egg', 'carrots', 'oil']),
		Recipe(rec_name='ramen', rec_ing_list=[
				'noodles', 'sliced beef', 'egg', 'ramen broth'])
	])


session.commit()  # writes changes to DB

all_recipe = session.query(Recipe).all()
all_recipe  # prints everything retrieved

session.rollback()  # only rolls back stuff that hasn't been committed

# %% Make relationships

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric

class Ingredient(Base):
	__tablename__ = 'ingredients'
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	type = Column(String, nullable=False)
#	id_ing_rec = Column(Integer, ForeignKey('x_ing_rec.id'))  # don't need
	# Foreign Key should only use against table containing primary key column

# need a cross table to join the Ingredients and the Classes
class Recipe_Ingredient(Base):
	__tablename__ = 'x_rec_ing'
	id = Column(Integer, primary_key=True)
	ing_id = Column(Integer, ForeignKey('ingredients.id'))
	rec_id = Column(Integer, ForeignKey('recipes.id'))
	ing_qty = Column(Numeric)

class Recipe(Base):
	__tablename__ = 'recipes'
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)



thai_porridge = Recipe(name='thai porridge')
session.add(thai_porridge)
session.new

ing_list = []
ing_list.append(Ingredient(name='Rice', type='grains'))
ing_list.append(Ingredient(name='Mince', type='meat'))
ing_list.append(Ingredient(name='Fish Sauce', type='Sauce'))
[session.add(i) for i in ing_list]  # one way to add all
session.rollback()  # kick them out

session.add_all(ing_list)  # another way to add all

query = session.query(Ingredient).filter(Ingredient.name.like('%in%')).\
		order_by(Ingredient.id)
query = session.query(Ingredient).filter(Ingredient.name.like('%in%'))

query.all()
query.first()
query.one()

session.commit()

# %% Have to figure out what happens when the session drops

# %% Bi-direction many to many
from sqlalchemy import create_engine
engine = create_engine("postgresql://hungy:1234qwer@localhost/food_db", echo=True)

# the class that links python classes to SQL tables
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Numeric, Column, Integer, String, ARRAY  # case sensitive
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Association(Base):
    __tablename__ = 'association'
    left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child", back_populates="parents")
    parent = relationship("Parent", back_populates="children")

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Association", back_populates="parent")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
    parents = relationship("Association", back_populates="child")

Base.metadata.tables

engine = create_engine("postgresql://hungy:1234qwer@localhost/food_db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()


# %%
# create parent, append a child via association
p = Parent()
a = Association(extra_data="some data")
a2 = Association(extra_data="another test")

a.child = Child()
a2.child = Child()
p.children.append(a)
p.children.append(a2)


# iterate through child objects via association, including association
# attributes
for assoc in p.children:
    print(assoc.extra_data)
    print(assoc.child)

session.add_all([p, a])
session.commit()

# %%

Base.metadata.drop_all(engine)
