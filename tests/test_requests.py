from models.city_weather import CityWeather
from datetime import datetime, timedelta

def test_query( get_db, get_client ):
    get_db.session.add( CityWeather( 'Paris', 'Cloudy', 293 ) )
    get_db.session.add( CityWeather( 'Tokyo', 'Rainy', 282 ) )
    get_db.session.add( CityWeather( 'Sao Paulo', 'Sunny', 297 ) )
    old_entry = CityWeather( 'London', 'Foggy', 280 )
    old_entry.date = datetime.now() - timedelta( minutes=30 )
    get_db.session.add( old_entry )
    get_db.session.commit()
    response = get_client.get( '/weather?max_entries=4' )
    assert isinstance( response.json, list )
    assert len(response.json) == 3

def test_insertion( get_client ):
    response = get_client.get( '/weather/Lisbon' )
    assert isinstance( response.json, dict )
    assert CityWeather.query.filter( CityWeather.city=='Lisbon' ).first()
