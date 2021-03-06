from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_cors import CORS

db = SQLAlchemy()

def create_app( **config_overrides ):
   app = Flask( __name__ )
   CORS( app )#, resources={ '/*':{ 'origins':'http://localhost:8081' } } )
    
   app.config.from_pyfile( 'settings.py' )
   app.config.update( config_overrides )

   db.init_app( app )
   Migrate( app, db )
    
   from controllers.weather_search import weather
   app.register_blueprint( weather )
    
   return app

if __name__ == "__main__":
   app = create_app()
   app.run( host='0.0.0.0', port=5000 )
