from app import orm
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# This file contains the snowflake schema required for maintaining all information

# Changes were made for LDAP
# DO NOT CHANGE
class User(UserMixin, orm.Model):
	__tablename__ = 'users'
	__table_args__ = (
		orm.PrimaryKeyConstraint('user_id'),
	)
	user_id = orm.Column(orm.String(50), primary_key = True)
	name = orm.Column(orm.String(50))
	password_hash = orm.Column(orm.String(128), nullable = False)
	status = orm.Column(orm.String(1))# N for new, A for active, D for deleted
	last_login = orm.Column(orm.DateTime, default=datetime.datetime.utcnow)
	def create(self, **kwargs):
		self.password_hash = generate_password_hash(kwargs['password'])
		orm.session.add(self)
		orm.session.commit()
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
		orm.session.commit()
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	def is_deleted(self):
		if self.status == 'D':
			return True
		return False
	def is_new(self):
		if self.status == 'N':
			return True
		return False
	def is_approved(self):
		if self.status == 'A':
			return True
		return False
	def approve_user(self):
		if self.status == 'N':
			self.status = 'A'
			return True
		return False
	def get_id(self):
		return self.user_id
	def __repr__(self):
		return '<User object id = {}>'.format(self.user_id)

class ChatMessage(orm.Model):
	__tablename__ = 'chat_message'
	__table_args__ = (
		orm.PrimaryKeyConstraint('user_id', 'timestamp'),
	)
	user_id = orm.Column(orm.String(50), orm.ForeignKey('users.user_id'))
	message = orm.Column(orm.String(200), nullable=False)
	timestamp = orm.Column(orm.DateTime, nullable=False, server_default=orm.func.now())
