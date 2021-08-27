from app import db
from datetime import datetime

class CityWeather( db.Model ):
    __tablename__ = "CitiesWeather"
    city = db.Column( db.String, primary_key=True )
    weather = db.Column( db.String )
    temperature = db.Column( db.Integer )
    date = db.Column( db.DateTime )
    
    def __init__( self, city, weather, temp ):
        self.set( city, weather, temp )

    def set( self, city, weather, temp ):
        self.city = city
        self.weather = weather
        self.temperature = temp
        self.date = datetime.now()