import os
import datetime
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:  DATABASE = SqliteDatabase('listings.sqlite')

  # OPTIONALLY: instead of the above line, here's how you could have your 
  # local app use PSQL instead of SQLite:

  # DATABASE = PostgresqlDatabase('dog_demo', user='reuben')  

  # the first argument is the database name -- YOU MUST MANUALLY CREATE 
  # IT IN YOUR psql TERMINAL
  # the second argument is your Unix/Linux username on your computer

class Agent(UserMixin, Model):
	first_name = CharField()
	last_name = CharField()
	email = CharField(unique=True)
	password = CharField()
	phone_number = CharField(unique=True)
	company_name = CharField()
	# member_since = DateTimeField(default=datetime.datetime.now)

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