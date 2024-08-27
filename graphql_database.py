# Importing all the necessary modules
import json

from graphene import Mutation, ObjectType, Field, String, List, Schema
from mysql.connector import connect

# Establishing the database connection and selecting the table
db = connect(host='localhost', user='root', password='MySQL@1', database='To_Do')
cur = db.cursor()
cur.execute('use To_Do')


# Function to get userinfo from the json file
def getuserinfo():
	"""This function is used to get the userinfo saved by 'server.py' in the 'userinfo.json' file & then returns the
	information in form of dictionary."""
	f = open('userinfo.json', 'r')
	data = json.loads(f.read())
	f.close()
	return data


# Class to define model of the To_Do table of the database
class ToDo(ObjectType):
	title = String()
	description = String()
	time = String()
	images = String()


# Class for retrieving a single to-do or all to-do using the graphql structure
class Query(ObjectType):
	"""This is the query class of graphql which executes the MySQL query embedded in the graphql query structure to
	get a single To-Do (by to-do title) or list of all To-Dos from the database, for specified user."""
	todo = Field(ToDo, title=String())

	def resolve_todo(self, info, title):
		cur.execute(
			f'SELECT title, description, time, images FROM To_Do where title="{title}" and userid="{getuserinfo()["sub"]}"')
		result = cur.fetchone()
		return {'title': result[0], 'description': result[1], 'time': result[2], 'images': result[3]}

	todos = List(ToDo)

	def resolve_todos(self, info):
		cur.execute(f'SELECT title, description, time, images FROM To_Do where userid="{getuserinfo()["sub"]}"')
		result = cur.fetchall()
		result_json = []
		for i in range(len(result)):
			result_json.append(
				{'title': result[i][0], 'description': result[i][1], 'time': result[i][2], 'images': result[i][
					3]})
		return result_json


# Class for adding a single to-do into the database using the graphql structure
class CreateToDo(Mutation):
	"""This is the mutation class of graphql which executes the MySQL query to add a new To-Do into the database
	embedding it the graphql
	query structure for the specified user."""
	class Arguments:
		title = String()
		description = String()
		time = String()
		images = String()

	todo = Field(lambda: ToDo)

	def mutate(self, info, title, description, time, images):
		if images != '':
			cur.execute(f'INSERT INTO To_Do (userid, title, description, time, images) VALUES ("'
			            f'{getuserinfo()["sub"]}", "{title}", '
			            f'"{description}", '
			            f'"{time}", '
			            f'"{images}")')
			db.commit()
		else:
			cur.execute(f'INSERT INTO To_Do (userid, title, description, time) VALUES ("{getuserinfo()["sub"]}", "{title}", "{description}", '
			            f'"{time}")')
			db.commit()
		todo = ToDo(title=title, description=description, time=time, images=images)
		return CreateToDo(todo=todo)


# Class for updating a single to-do into the database using the graphql structure
class UpdateToDo(Mutation):
	"""This is the mutation class of graphql which executes the MySQL query to update a To-Do into the database
		embedding it the graphql
		query structure for the specified user."""
	class Arguments:
		title = String()
		description = String()
		time = String()
		images = String()

	todo = Field(lambda: ToDo)

	def mutate(self, info, title, description, time, images):
		if images == '':
			cur.execute(f'UPDATE To_Do SET description="{description}", time="{time}" WHERE title="{title}" and '
			            f'userid="{getuserinfo()["sub"]}"')
			db.commit()
		else:
			cur.execute(
				f'UPDATE To_Do SET description="{description}", time="{time}", images="{images}" WHERE title="'
				f'{title}" and userid="{getuserinfo()["sub"]}"')
			db.commit()
		todo = ToDo(title=title, description=description, time=time, images=images)
		return UpdateToDo(todo=todo)


# Class for deleting a single to-do into the database using the graphql structure
class DeleteToDo(Mutation):
	"""This is the mutation class of graphql which executes the MySQL query to delete a To-Do into the database
		embedding it the graphql
		query structure for the specified user."""
	class Arguments:
		title = String()

	todo = Field(lambda: ToDo)

	def mutate(self, info, title):
		cur.execute(f'DELETE FROM To_Do WHERE title="{title}" and userid="{getuserinfo()["sub"]}"')
		db.commit()
		todo = ToDo(title=title)
		return DeleteToDo(todo=todo)


# This is the mutation class, merging all the mutations together
class Mutation(ObjectType):
	create_todo = CreateToDo.Field()
	update_todo = UpdateToDo.Field()
	delete_todo = DeleteToDo.Field()


# Creating the schema
schema = Schema(query=Query, mutation=Mutation)
