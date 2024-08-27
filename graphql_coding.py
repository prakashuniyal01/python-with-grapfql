# Importing the schema, cursor, database connection and userinfo function
from graphql_database import schema, cur, db, getuserinfo


# Function to execute the graphql query for adding single to-do
def add_to_do(title, description, time, images=''):
	"""This function executes the graphql query to add a new To-Do to the database, with the details: title,
	description, time and images(for pro only)."""
	try:
		schema.execute("mutation{" +
		               f'createTodo(title: "{title}", description: "{description}", time: "{time}", images: "{images}")' +
		               "{todo{title description time images}}}")
		return 'True'
	except Exception as e:
		return e


# Function to execute the graphql query for updating single to-do
def update_to_do(title, description, time, images):
	"""This function executes the graphql query to update description or time or images(for pro only) of a To-Do from the
	database
	based on the To-Do
	title requested by the user."""
	try:
		schema.execute("mutation{" +
		               f'updateTodo(title: "{title}", description: "{description}", time: "{time}", images: "{images}")' +
		               "{todo{title description time images}}}")
		return
	except Exception as e:
		pass
	return


# Function to execute the graphql query for deleting single to-do
def delete_to_do(title):
	"""This function executes the graphql query to delete a To-Do from the database based on the To-Do title
	requested by the user."""
	schema.execute("mutation{" +
	               f'deleteTodo(title: "{title}")' +
	               "{todo{title}}}")
	return


# Function to execute the graphql query for showing single to-do
def show_to_do(title):
	"""This function executes a graphql query to return a single To-Do from the database based on the To-Do title
	requested by the user"""
	try:
		result = schema.execute("query{" +
		                        f'todo(title: "{title}")' +
		                        "{title description time images}}")
		if result.data['todo'] is None:
			return 'None'
		else:   
			return {'title': result.data['todo']['title'], 'description': result.data['todo']['description'],
			         'time': result.data['todo']['time'], 'images': result.data['todo']['images']}
	except Exception as e:
		return e


# Function to execute the graphql query for showing all to-dos
def show_to_dos():
	"""This function executes a graphql query to return all the To-Dos from the database for the specified user."""
	displaytodos = schema.execute('''
		query {
			todos{
				title
				description
				time
				images
			}
		}
	''')
	return displaytodos.data['todos']


# Function to get pro attribute state
def ispro():
	"""This function execute a MySQL query to get the pro attribute state & return it to 'server.py'. It returns
	'True' or 'False' where 'True' = Purchased Pro License & 'False' = Not Purchased Pro License."""
	cur.execute(f'SELECT pro from To_Do where userid="{getuserinfo()["sub"]}"')
	result = cur.fetchall()
	if len(result) == 0:
		return 'False'
	return result[0][0]


# Function to get name of user
def send_userinfo():
	"""This function reads the 'userinfo.json' to get its name & return to the 'server.py' to display it on the
	navigation
	bar."""
	return getuserinfo()["name"]


# Function to change pro attribute
def update_to_pro():
	"""This function executes the MySQL query to update the pro attribute of the user to 'True' when he/she has
	successfully purchased the pro-license."""
	cur.execute(f'UPDATE To_Do set pro="True" where userid="{getuserinfo()["sub"]}"')
	db.commit()
