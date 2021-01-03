import sqlite3
import pandas
import numpy


class DataBase(object):
	# connects (or creates) to the database
	def __init__(self):
		self.connection = sqlite3.connect('components/messages.db', check_same_thread=False)
		self.cursor = self.connection.cursor()

	# creates table for user if not exists
	def create_table(self, user):
		command = f"CREATE TABLE IF NOT EXISTS {user}_table (id INTEGER PRIMARY KEY AUTOINCREMENT, \
			user VARCHAR(20), date DATE)"
		self.cursor.execute(command)

	# appends new message to table
	def append(self, user, msg, date):
		command = f"INSERT INTO {user}_table (user, date) VALUES (?, ?)"
		if msg != "":
			self.cursor.execute(command, (msg, date))
			self.connection.commit()

	# returns all messages sent by the user
	def get(self, user):
		command = f"SELECT * FROM {user}_table"
		messages = pandas.read_sql_query(command, self.connection)
		return numpy.array(messages)

	# deletes all records from user
	def drop_table(self, user):
		command = f"DROP TABLE {user}_table"
		self.cursor.execute(command)
