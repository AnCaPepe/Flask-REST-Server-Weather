from flask import Blueprint, request, redirect, url_for, session
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import json

from models.city_weather import CityWeather
from app import db

weather = Blueprint( 'weather', __name__ )

@weather.route( '/', methods=[ 'GET' ] )
def get_list_from_cache():
    max_entries = request.args.get( 'max', default=5, type=int )
    return json.dump( {} )

@weather.route( '/<string:city>', methods=[ 'GET' ] )
def get_for_city( city ):
    return json.dump( {} )