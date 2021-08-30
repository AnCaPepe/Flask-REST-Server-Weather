from flask import Blueprint, request, redirect, jsonify, make_response, current_app
from flask_cors import cross_origin
from datetime import datetime, timedelta
import requests
import sqlalchemy

from models.city_weather import CityWeather
from app import db

MAX_ENTRIES_DEFAULT = 5
ENTRY_TIMEOUT = 5

weather = Blueprint( 'weather', __name__ )

def query_cities( max_entries, timeout_min ):
    try:
        date_start = datetime.now() - timedelta( minutes=timeout_min )
        entries = CityWeather.query.filter( CityWeather.date > date_start )
        entries = entries.order_by( CityWeather.date.desc() ).slice( 0, max_entries ).all()
    except sqlalchemy.exc.SQLAlchemyError as e:
        raise Exception( str(e) )
    return entries

@weather.route( '/weather', methods=[ 'GET' ] )
def get_list_from_cache():
    try:
        max_entries = request.args.get( 'max', default=MAX_ENTRIES_DEFAULT, type=int )
        entries = query_cities( max_entries, ENTRY_TIMEOUT )
    except requests.exceptions.RequestException as e:
        print( e )
        return make_response( e, 400 )
    except BaseException as e:
        print( e )
        return make_response( e, 500 )

    results = []
    for entry in entries:
        results.append( { 'city':entry.city, 'weather':entry.weather, 'temperature':entry.temperature } )

    response = jsonify( results )
    response.headers.add( "Access-Control-Allow-Origin", "*" )
    return make_response( response, 200 )

def insert_city( city_name, weather_description, temperature ):
    try:
        entry = CityWeather.query.filter( CityWeather.city==city_name ).first()
        if not entry: 
            entry = CityWeather( city_name, weather_description, temperature )
            db.session.add( entry )
        else:
            entry.set( city_name, weather_description, temperature )
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        raise Exception( str(e) )

    return entry

@weather.route( '/weather/<string:city>', methods=[ 'GET' ] )
def get_for_city( city ):
    try:
        print( current_app.config[ 'API_KEY' ] )
        params = { 'q':city, 'appid':current_app.config[ 'API_KEY' ] }
        data = requests.get( 'https://api.openweathermap.org/data/2.5/weather', params=params ).json()
        city_name = data['name']
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        entry = insert_city( city_name, weather_description, temperature )
    except requests.exceptions.RequestException as e:
        print( e )
        return make_response( e, 400 )
    except BaseException as e:
        print( e )
        return make_response( e, 500 )

    result = { 'city':entry.city, 'weather':entry.weather, 'temperature':entry.temperature }

    response = jsonify( result )
    response.headers.add( "Access-Control-Allow-Origin", "*" )
    return make_response( response, 200 )