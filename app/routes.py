from functools  import wraps
from app import login_manager, application
from flask import redirect, render_template, url_for, abort, flash, make_response, request
from flask_login import login_required, login_user, logout_user, current_user

from app.models import *
from app import orm
import pandas

#Get the login_manager and the application to register routes
# Import flask specific components

def validate_form(template_form, redirect_url, args={}):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			form = template_form()
			if not form.validate_on_submit():
				print('Invalid form submission', form.errors, form.data)
				return render_template(redirect_url, form=form, error='Enter appropriate details', **kwargs)
			# This hides the part where any information submitted is checked for injection.
			return func(form)
		return wrapper
	return decorator

# Relatively import the forms for login
from . import forms, models

# This is the component that loads the user, do not make changes to this
# If the application fails to load a user, subsequent checks automatically fail
# causing an error page
@login_manager.user_loader
def user_loader(id):
	try:
		user = models.User.query.filter_by(user_id=id).first()
		if user:
			return user
		else:
			return None
	except Exception as e:
		return None

# Redirect logic for the 1st layer of security.
# No matter from where you enter, you shall be shown the door to enter.
@login_manager.unauthorized_handler
def unauthorized():
	print('Unauthorized execute')
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
		# return redirect(url_for('login'))

# GET methods only have sanity check and page delivery
@application.route('/login', methods=['GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = forms.LoginForm()
	return  render_template('login.jinja2', form=form)

# Login process
# Only approved user can acquire the rights to gain access to the system
# If they haven't been approved, they will not be able to access anything
@application.route('/login', methods=['POST'])
@validate_form(forms.LoginForm, 'login.jinja2')
def login_post(form): # Main login logic
	# Main logic
	user = models.User.query.filter_by(user_id=form.user_id.data).first()
	if user:
		if user.check_password(form.password.data):
			print('Login', user)
			login_user(user)
			return redirect(url_for('chatroom'))
		else:
			return render_template('login.jinja2', form=form, error='Wrong credentials')
	else:
		return render_template('login.jinja2', form=form, error='Wrong credentials')

# GET methods for signup
@application.route('/signup', methods=['GET'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = forms.SignupForm()
	return render_template('signup.jinja2', form=form)

# Signup process
# On signup a user is created and marked as new(N) in the User model
# This user needs to be approved(A) before they gain the ability to access anything
# The only addition that may be required is the creation of a captcha to prevent
# DDoS and pranks
@application.route('/signup', methods=['POST'])
@validate_form(forms.SignupForm, 'signup.jinja2')
def signup_post(form):
	user = models.User(
		user_id=form.user_id.data,
		name=form.name.data,
		status = 'A'
	)
	user.create(password=form.password.data)
	return redirect(url_for('login'))

# Process to log user out
@application.route('/logout')
@login_required
def logout():
	logout_user()
	form = forms.LoginForm()
	return render_template('login.jinja2',form=form, error='You have been logged out')

@application.route('/')
@login_required
def chatroom():
	return render_template('base.jinja2')

@application.route('/send', methods=['POST'])
@login_required
def send_message():
	user_id = current_user.user_id
	message = request.form['message']
	message = ChatMessage(user_id = user_id, message = message)
	orm.session.add(message)
	orm.session.commit()
	return 'OK', 200

@application.route('/fetch', methods=['POST'])
@login_required
def fetch():
	query = 'SELECT * FROM chat_message ORDER BY timestamp ASC;'
	users = pandas.read_sql(query, orm.get_engine(application).connect())
	json_str = users.tail(50).to_json(orient='records')
	response = make_response(json_str)
	response.mimetype = 'text/json'
	return response
