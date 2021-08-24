from app import db
from datetime import datetime

class CityWeather( db.Model ):
    __tablename__ = "CitiesWeather"
    city = db.Column( db.String, primary_key=True )
    weather = db.Column( db.String )
    date = db.Column( db.DateTime )
    
    def __init__( self, city, weather ):
        self.city = city
        self.weather = weather
        self.date = datetime.now()