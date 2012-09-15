import mongoengine

class Weather(mongoengine.Document):
    created = mongoengine.DateTimeField()
    latitude = mongoengine.DecimalField()
    longitude = mongoengine.DecimalField()
    model_name = mongoengine.StringField()
    meta = {
        'allow_inheritance': True
    }

class Precipitation(Weather):
    date_from = mongoengine.DateTimeField(required=True)
    date_to = mongoengine.DateTimeField(required=True)
    precipitation = mongoengine.DecimalField()
    symbol = mongoengine.IntField(min_value=1, max_value=23)

class State(Weather):
    at = mongoengine.DateTimeField(required=True)
    temperature = mongoengine.DecimalField()
    wind_direction = mongoengine.StringField()
    wind_angle = mongoengine.DecimalField()
    wind_speed = mongoengine.DecimalField()
    humidity = mongoengine.DecimalField()
    pressure = mongoengine.DecimalField()
    cloudiness = mongoengine.DecimalField()
    fog = mongoengine.DecimalField()
    low_clouds = mongoengine.DecimalField()
    medium_clouds = mongoengine.DecimalField()
    high_clouds = mongoengine.DecimalField()