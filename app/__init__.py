# We'll be designing a role manager for our own purposes
# An inbuilt Device Fingerprinting method is required to ensure secure operations throughout.
import os
# The main flask components
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
# The background scheduler that will be used to schedule jobs

# globally declared importable variables instances
application = Flask(__name__,
	template_folder = os.path.join(os.getcwd(), 'frontend', 'templates'),
	static_folder = os.path.join(os.getcwd(), 'frontend', 'static')
)# Add the template_folder and static_folder
orm = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
# Since this exists in the lifetime of the application, we can add more jobs to it without a problem.
# scheduler = BackgroundScheduler()
# Developers need to see what Jobs are scheduled however.
# This is available through a frontend utilities only to the workbench devs

# Application creation logic
def create(jobs_schema=''):
	global application, orm, login_manager
	import config
	application.config.update(**config.config)
	application.config.update(SECRET_KEY = os.urandom(32))
	from app import routes, models
	orm.init_app(application)
	login_manager.init_app(application)
	csrf.init_app(application)
	with application.app_context():
		orm.create_all(bind=None)
	# Read everything, before changing the context https://readthedocs.org/projects/flask-sqlalchemy/downloads/pdf/master/
	return application
