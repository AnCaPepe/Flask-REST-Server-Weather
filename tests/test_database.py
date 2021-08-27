from models.city_weather import CityWeather

def test_model():
    entry = CityWeather( 'London', 'cloudy', 284 )
    assert entry.city == 'London'
    assert entry.weather == 'cloudy'
    assert entry.temperature == 284

def test_insertion( get_db ):
    entry = CityWeather( 'Sao Paulo', 'sunny', 293 )
    get_db.session.add( entry )
    get_db.session.commit()
    entry = CityWeather.query.filter( CityWeather.city=='Sao Paulo' ).first()
    assert entry
    assert entry.city == 'Sao Paulo'