from django.utils.translation import ugettext_lazy as _

import mongoengine

SYMBOLS = (
    (1, _("Sun")),
    (2, _("Light cloud")),
    (3, _("Partly cloud")),
    (4, _("Cloud")),
    (5, _("Light rain and sun")),
    (6, _("Light rain, thunder and sun")),
    (7, _("Sleet and sun")),
    (8, _("Snow and sun")),
    (9, _("Light rain")),
    (10, _("Rain")),
    (11, _("Rain and thunder")),
    (12, _("Sleet")),
    (13, _("Snow")),
    (14, _("Snow and thunder")),
    (15, _("Fog")),
    (16, _("Sun (used for winter darkness)")),
    (17, _("Light cloud ( winter darkness )")),
    (18, _("Light rain and sun")),
    (19, _("Snow and sun ( used for winter darkness )")),
    (20, _("Sleet, sun and thunder")),
    (21, _("Snow, sun and thunder")),
    (22, _("Light rain and thunder")),
    (23, _("Sleet thunder")),
)

# TODO: Some fields have to be unique to make sure that there is only one entry for each time period for given location. 
# https://github.com/wlanslovenija/PiplMesh/issues/210
class Weather(mongoengine.Document):
    created = mongoengine.DateTimeField(required=True)
    latitude = mongoengine.DecimalField(required=True)
    longitude = mongoengine.DecimalField(required=True)
    model_name = mongoengine.StringField(required=True)
    
    meta = {
        'allow_inheritance': True,
    }

class Precipitation(Weather):
    date_from = mongoengine.DateTimeField(required=True)
    date_to = mongoengine.DateTimeField(required=True)
    precipitation = mongoengine.DecimalField(required=True)
    symbol = mongoengine.IntField(choices=SYMBOLS, required=True)

class State(Weather):
    at = mongoengine.DateTimeField(required=True)
    temperature = mongoengine.DecimalField(required=True)
    wind_direction = mongoengine.StringField(required=True)
    wind_angle = mongoengine.DecimalField(required=True)
    wind_speed = mongoengine.DecimalField(required=True)
    humidity = mongoengine.DecimalField(required=True)
    pressure = mongoengine.DecimalField(required=True)
    cloudiness = mongoengine.DecimalField(required=True)
    fog = mongoengine.DecimalField(required=True)
    low_clouds = mongoengine.DecimalField(required=True)
    medium_clouds = mongoengine.DecimalField(required=True)
    high_clouds = mongoengine.DecimalField(required=True)