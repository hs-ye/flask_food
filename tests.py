# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 20:13:29 2018
Testing for the SQLAlchemy ORM with Postgres backend
Does NOT use the SQLAlchemy Expression Language
@author: yehan
"""
# %% Pure SQLAlchemy Tests, no flask involved

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import  relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# the 'base' class that all 'classes', i.e. table representations
# In the ORM inherit
Base = declarative_base()

class Recipes(Base):
	__tablename__ = 'test_rec'  # will make the table called
	id = Column(Integer, primary_key=True)
	name = Column(String)

	# don't need to explicitly define __init__

class Ingredients(Base):
	__tablename__ = 'ingredient'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	recipe_id = Column(Integer, ForeignKey('test_rec.id'))
	recipe = relationship(Recipes, backref=backref('ingredients', uselist=True))

# Setup core interface to Database
engine = create_engine('postgresql\
	://postgres:1234qwer@localhost/food_db', echo=True)
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)  # creates all tables as defined by the classes, against 'Base' object

# %% Pure SQLAlchemy add and retrieve recipes (this is a test data model...)
rice = Ingredients(name='rice')
congee = Recipes(name='Congee')
rice.recipe = congee
s = session()
s.add(rice)
s.add(congee)
s.commit()

# %% Retrieve data
from sqlalchemy import select

results = s.execute(select([Ingredients.id]).where(Ingredients.name == 'rice'))
results

results.fetchone()

s.close() # closes connection


# %% Metadata - contains info about db tables, like the 'information_schema' table
from sqlalchemy import MetaData

# Makes a new metadata object. Current python engine will only know
# about the tables that have been linked through this Metadata obj instance
# this instance also used to make
metadata = MetaData()

for t in metadata.sorted_tables:
	print(t.name)
# doesn't seem to work for tables defined using the class system




