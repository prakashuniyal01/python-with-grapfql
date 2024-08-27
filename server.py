# Importing all required modules and their functions
import logging
from flask_oidc import OpenIDConnect
from keycloak import KeycloakOpenID

import stripe
from flask import Flask, render_template, redirect, g, request

from graphql_coding import add_to_do, show_to_do, show_to_dos, delete_to_do, update_to_do, update_to_pro, ispro, \
	send_userinfo

stripe.api_key = "<YOUR STRIPE API KEY>"  # Replace the stripe API key with YOUR OWN STRIPE API KEY as a string without any angular brackets
app = Flask(__name__, static_folder='./static', template_folder='templates')

# Configuring the app with keycloak credentials
logging.basicConfig(level=logging.DEBUG)
app.config.update({
	'SECRET_KEY': '<YOUR CLIENT SECRET KEY>',  # Replace the keycloak CLIENT SECRET key with YOUR OWN CLIENT SECRET KEY as a string without any angular brackets
	'TESTING': True,
	'DEBUG': True,
	'OIDC_CLIENT_SECRETS': 'client_secrets.json',
	'OIDC_ID_TOKEN_COOKIE_SECURE': False,
	'OIDC_REQUIRE_VERIFIED_EMAIL': False,
	'OIDC_USER_INFO_ENABLED': True,
	'OIDC_OPENID_REALM': 'myorg',
	'OIDC_SCOPES': ['openid', 'email', 'profile'],
	'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})
oidc = OpenIDConnect(app)
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/", client_id="test_api_client",
                                 realm_name="myorg", client_secret_key=',YOUR CLIENT SECRET KEY.')  # # Replace the keycloak CLIENT SECRET key with YOUR OWN CLIENT SECRET KEY as a string without any angular brackets


# 404 Error is handled here
@app.errorhandler(404)
def not_found(e):
	return ('<div style="text-align: center; margin-top: 25%; color: red"><h1>PAGE NOT FOUND<br><button>'
	        '<a ''href="/" style="text-decoration: none; color: green"><h2>Click to ' \
	        'go to Home ' \
	        'Page</h2></a></button></h1></div>')


# ------------------------------
# Routes begin from here
# This is the route for home
@app.route('/')
def home():
	if oidc.user_loggedin and ispro() == 'True':  # render home page, when user is pro licensed and logged in
		return render_template('index.html', logged=True, pro=True, name=send_userinfo())
	elif oidc.user_loggedin and ispro() == 'False':  # render home page, when user is not pro licensed and logged in
		return render_template('index.html', logged=True, pro=False, name=send_userinfo())
	else:  # render home page, when user is not logged in
		return render_template('index.html', logged=False)


# This is the route for login
@app.route('/login')
@oidc.require_login  # calls the keycloak login page for user login/register
def login():
	f = open('userinfo.json', 'w')  # write user details in a json file locally
	info = oidc._retrieve_userinfo()
	f.write('{' +
	        f'"sub": "{info["sub"]}", "name": "{info["name"]}", "username": '
	        f'"{info["preferred_username"]}", '
	        f'"email": "{info["email"]}"' +
	        '}')
	f.close()
	return redirect('/')


# This is the route for logout
@app.route('/user/logout')
def logout():  # logs the user out of the keycloak user-session
	refresh_token = oidc.get_refresh_token()
	oidc.logout()
	if refresh_token is not None:  # refreshes the user token to log out
		keycloak_openid.logout(refresh_token)

	oidc.logout()
	g.oidc_id_token = None
	return redirect('/')


# This is the route to display all the To-Dos
@app.route('/user/list-all-To-Dos')
def showalltodo():
	if oidc.user_loggedin and ispro() == 'True':  # executing when user logged in and is a pro licensed
		data = show_to_dos()
		return render_template('listAllToDo.html', data=data, logged=True, pro=True, name=send_userinfo())
	elif oidc.user_loggedin and ispro() == 'False':  # executing when user logged in and is not a pro licensed
		data = show_to_dos()
		return render_template('listAllToDo.html', data=data, logged=True, pro=False, name=send_userinfo())
	else:
		return redirect('/')


# This is the route to display a single To-Do
@app.route('/user/list-a-To-Do', methods=['GET', 'POST'])
def showatodo():
	if oidc.user_loggedin and ispro() == 'True':  # when user logged in and is a pro licensed
		if request.method == 'POST':
			data = show_to_do(request.form.get('title'))
			if data == 'None':
				return render_template('listOneToDo.html', data=None, logged=True, pro=True, name=send_userinfo())
			return render_template('listOneToDo.html', data=data, logged=True, pro=True, name=send_userinfo())
		return render_template('listOneToDo.html', data=None, logged=True, pro=True, name=send_userinfo())

	elif oidc.user_loggedin and ispro() == 'False':  # when user logged in and is not a pro licensed
		if request.method == 'POST':
			data = show_to_do(request.form.get('title'))
			if data == 'None':
				return render_template('listOneToDo.html', data=None, logged=True, pro=False, name=send_userinfo())
			return render_template('listOneToDo.html', data=data, logged=True, pro=False, name=send_userinfo())
		return render_template('listOneToDo.html', data=None, logged=True, pro=False, name=send_userinfo())
	else:
		return redirect('/')


# This is the route to add a To-Do
@app.route('/user/add-a-To-Do', methods=['GET', 'POST'])
def addatodo():
	if oidc.user_loggedin and ispro() == 'True':  # executing when user logged in and pro licensed
		if request.method == 'POST':
			result = add_to_do(title=request.form.get('title'), description=request.form.get('description'),
			                   time=request.form.get('time'), images=request.form.get('images'))
			if result == 'True':
				data = show_to_do(request.form.get('title'))
				return render_template('listOneToDo.html', data=data, logged=True, pro=True, name=send_userinfo())
			else:
				return redirect('/user/add-a-To-Do', logged=True, pro=True, name=send_userinfo())
		return render_template('addAToDo.html', logged=True, pro=True, name=send_userinfo())
	elif oidc.user_loggedin and ispro() == 'False':  # executing when user logged in and not pro licensed
		if request.method == 'POST':
			result = add_to_do(title=request.form.get('title'), description=request.form.get('description'),
			                   time=request.form.get('time'), images=request.form.get('images'))
			if result == 'True':
				data = show_to_do(request.form.get('title'))
				print(data)
				return render_template('listOneToDo.html', data=data, logged=True, pro=False, name=send_userinfo())
			else:
				return redirect('/user/add-a-To-Do', logged=True, pro=False, name=send_userinfo())
		return render_template('addAToDo.html', logged=True, pro=False, name=send_userinfo())
	else:
		return redirect('/')


# This is the route to edit a To-Do
@app.route('/user/edit-a-To-Do/<title>', methods=['GET', 'POST'])
def editatodo(title):
	if oidc.user_loggedin and ispro() == 'True':  # executing this when user logged in and is a pro licensed
		if request.method == 'POST':
			update_to_do(title=request.form.get('title'), description=request.form.get('description'),
			             time=request.form.get('time'),
			             images=request.form.get('images'))
			return redirect('/user/list-all-To-Dos')

		data = show_to_do(title)
		return render_template('editAToDo.html', data=data, logged=True, pro=True, name=send_userinfo())
	elif oidc.user_loggedin and ispro() == 'False':  # executing this when user logged in and is not a pro licensed
		if request.method == 'POST':
			update_to_do(title=request.form.get('title'), description=request.form.get('description'),
			             time=request.form.get('time'),
			             images='')
			return redirect('/user/list-all-To-Dos')

		data = show_to_do(title)
		return render_template('editAToDo.html', data=data, logged=True, pro=False, name=send_userinfo())
	else:
		return redirect('/')


# This is the route to delete a To-Do
@app.route('/user/delete-a-To-Do/<title>', methods=['GET', 'POST'])
def deleteatodo(title):
	if oidc.user_loggedin:
		delete_to_do(title)
		return redirect('/user/list-all-To-Dos')
	else:
		return redirect('/')


# This is the route to buy a pro license using stripe test api
@app.route('/user/buy-pro-license')
def payment():
	if (oidc.user_loggedin and len(show_to_dos()) != 0):
		try:
			checkout = stripe.checkout.Session.create(
				line_items=[{
					'price': 'price_1NZUDkSBIuEMkI6UXfQrMy1y',
					'quantity': 1
				}],
				mode='subscription',
				success_url='http://localhost:5000/thankyou',
				cancel_url='http://localhost:5000/retrypay'
			)
			return redirect(checkout.url)

		except Exception as e:
			return f'ERROR: {e}'
	else:
		return ('<h1>FIRST ADD ATLEAST ONE TASK BEFORE PURCHASING THE PRO LICENSE</h1><br><h1><a href="/">Go To Home'
		        '</a></h1>')


# This is the route to display thank you page after the successful payment
@app.route('/thankyou')
def success():
	if oidc.user_loggedin:
		update_to_pro()
		return render_template('paysuccess.html')
	else:
		return redirect('/')


# This is the route to display retry payment page after the payment failure
@app.route('/retrypay')
def failed():
	if oidc.user_loggedin:
		return render_template('payfail.html')
	else:
		return redirect('/')


# Start the application
app.run()
