# The following are the configurations for the server. Change at your own peril.
import os
db_path = os.path.join(os.getcwd(), 'app.db')
config = {'SQLALCHEMY_DATABASE_URI': 'sqlite:///'+db_path, 'SQLALCHEMY_BINDS': {}, 'SQLALCHEMY_TRACK_MODIFICATIONS': False, 'PERMANANENT_SESSION_LIFETIME': 7776000.0, 'APPLICATION_ROOT': '/', 'PREFERRED_URL_SCHEME': 'https', 'JSON_AS_ASCII': True, 'JSON_SORT_KEYS': True, 'SESSION_COOKIE_NAME': 'programmers-chatroom.herokuapp.com', 'TRAP_HTTP_EXCEPTIONS': True, 'CAPTCHA_ENABLE': False, 'MAIL_ENABLE': False, 'LDAP_ENABLE': False, 'SUBNET_MASK': '24'}
