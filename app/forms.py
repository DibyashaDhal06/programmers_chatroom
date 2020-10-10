# Project ORDASH
# Module app.forms
# Author : Supratik Chatterjee
#
# This file is stable as of 23 May, 2019

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SelectMultipleField, IntegerField, HiddenField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email,ValidationError,Length
from app.models import User

class LoginForm(FlaskForm):
	user_id =  StringField('ID', validators=[DataRequired()],render_kw={"placeholder": "ID"})
	password = PasswordField('Password', validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder": "Password"})
	#recaptcha = RecaptchaField()

class SignupForm(FlaskForm):
	user_id =  StringField('ID', validators=[DataRequired()],render_kw={"placeholder": "ID"})
	name = StringField('Name', validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder": "User Name"})
	password = PasswordField('Password', validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder": "Password"})
