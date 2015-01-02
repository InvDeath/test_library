import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True,
SECRET_KEY = 'qwerty'

if 'FROM_ENV' in os.environ:
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', SQLALCHEMY_DATABASE_URI)
	SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)
