from flask import Blueprint, request, redirect, jsonify, make_response
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
from datetime import datetime, timedelta
import requests
import sqlalchemy

from models.city_weather import CityWeather
from app import db

weather = Blueprint( 'weather', __name__ )

@weather.route( '/weather', methods=[ 'GET' ] )
def get_list_from_cache():
    
    try:
        max_entries = request.args.get( 'max', default=5, type=int )
        entries = CityWeather.query.filter( CityWeather.date > datetime.now() - timedelta( minutes=5 ) )
        entries = entries.order_by( CityWeather.date.desc() ).slice( 0, max_entries ).all()
    except requests.exceptions.RequestException as e:
        print( e )
        make_response( e, 400 )
    except sqlalchemy.exc.SQLAlchemyError as e:
        print( e )
        make_response( e, 500 )
    except BaseException as e:
        print( e )
        make_response( e, 500 )

    results = []
    for entry in entries:
        results.append( { 'city':entry.city, 'weather':entry.weather, 'temperature':entry.temperature } )

    return make_response( jsonify( results ), 200 )

@weather.route( '/weather/<string:city>', methods=[ 'GET' ] )
def get_for_city( city ):

    try:
        params = { 'q':city, 'appid':'b7ad11c9717cd32f38612d368efaae1c' }#SECRET_KEY }
        data = requests.get( 'https://api.openweathermap.org/data/2.5/weather', params=params ).json()
        city_name = data['name']
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        entry = CityWeather.query.filter( CityWeather.city==city ).first()
        if not entry: 
            entry = CityWeather( city_name, weather_description, temperature )
            db.session.add( entry )
        else:
            entry.city = city_name
            entry.weather = weather_description
            entry.temperature = temperature
        db.session.commit()
    except requests.exceptions.RequestException as e:
        print( e )
        make_response( e, 400 )
    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        print( e )
        make_response( e, 500 )
    except Exception as e:
        print( e )
        make_response( e, 500 )

    result = { 'city':city_name, 'weather':weather_description, 'temperature':temperature }

    return make_response( jsonify( result ), 200 )