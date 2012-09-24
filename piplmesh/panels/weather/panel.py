from __future__ import absolute_import

import datetime

from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from piplmesh import nodes, panels

from . import models, weather

WEATHER_OBSOLETE = 6 # hours
FORECAST_HOUR = 14 # 14:00 o'clock or 2:00 PM

class WeatherPanel(panels.BasePanel): 
    def get_context(self, context):
        latitude = nodes.get_node(self.request).latitude
        longitude = nodes.get_node(self.request).longitude
        state = models.State.objects(latitude=latitude, longitude=longitude).order_by('+created').first()
        if state is None:
            context.update({
                'error_data': True,
            })
            return context
            
        context.update({
            'header': _("Weather"),
            'weather_objects': get_weather_content(latitude, longitude),
            'created': state.created,
        })
        return context

def get_weather_content(latitude, longitude):
    date = datetime.datetime.now()
    for interval in range(0, 3):
        state = models.State.objects(latitude=latitude, longitude=longitude, at__lte=date).order_by('-at').first()
        precipitation = models.Precipitation.objects(latitude=latitude, longitude=longitude, date_from__lte=date, date_to__gte=date).order_by('-date_from').first()
        weather_object = {
            'at': state.at,
            'temperature':  state.temperature,
            'symbol':  precipitation.symbol,
        }      
        date += datetime.timedelta(days=1)
        date = date.replace(hour=FORECAST_HOUR, minute=0)
        yield weather_object
          
panels.panels_pool.register(WeatherPanel)