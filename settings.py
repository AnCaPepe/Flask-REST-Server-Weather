import os
SECRET_KEY = os.environ.get( 'APP_SECRET_KEY', '\xbb\xe1I\xa0\xb7\xff.\x9f\x04\x0f0\xaf\xcb\x89j8' )
API_KEY = os.environ.get( 'API_SECRET_KEY', 'b7ad11c9717cd32f38612d368efaae1c' )
DB_HOST = os.environ.get( 'DB_HOST', 'localhost' )
DB_USERNAME = os.environ.get( 'DB_USERNAME', 'postgres' )
DB_PASSWORD = os.environ.get( 'DB_PASSWORD', 'postgres' )
DB_NAME = os.environ.get( 'DB_NAME', 'flaskapp_db' )
DB_URI = 'postgresql://%s:%s@%s:5432/%s' % ( DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME )
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
