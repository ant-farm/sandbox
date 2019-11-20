import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('listings.sqlite')

class Agent(UserMixin, Model):
	first_name = CharField()
	last_name = CharField()
	email = CharField(unique=True)
	password = CharField()
	phone_number = CharField(unique=True)
	company_name = CharField()

	class Meta:
		database = DATABASE

class Listing(Model):
	client_name = CharField()
	client_number = CharField(unique=True)
	property_address = CharField(unique=True)
	list_price = IntegerField()
	agent_id = ForeignKeyField(Agent, backref='agents')
	days_on_market = DateTimeField(default=datetime.datetime.now)
	

	class Meta: 
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Agent, Listing], safe=True)
	print("Created tables if they weren't already there")

	DATABASE.close()