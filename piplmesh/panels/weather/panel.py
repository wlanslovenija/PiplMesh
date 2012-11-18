import datetime

from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _

from piplmesh import nodes, panels

from . import models

WEATHER_OBSOLETE = 6 # 6 hours
FORECAST_HOUR = 14 # 14:00 o'clock or 2:00 PM
WEATHER_FORECAST_RANGE = 3 # days from being created

class WeatherPanel(panels.BasePanel): 
    def get_context(self, context):
        context.update({
            'header': _("Weather"),
        })
        
        latitude = self.request.node.latitude
        longitude = self.request.node.longitude
        # TODO: Check and possibly optimize
        state = models.State.objects(latitude=latitude, longitude=longitude, at__lte=datetime.datetime.now(), at__gte=(datetime.datetime.now() - datetime.timedelta(hours=WEATHER_OBSOLETE))).order_by('+created').first()
        if state is None:
            context.update({
                'error_data': True,
            })
            return context

        if timezone.now() >= state.created + datetime.timedelta(hours=WEATHER_OBSOLETE):
            context.update({
                'error_obsolete': True,
            })
            return context   
   
        context.update({
            'weather_objects': get_weather_content(latitude, longitude),
            'created': state.created,
        })
        return context

# TODO: Check and possibly optimize
def get_weather_content(latitude, longitude):
    date = datetime.datetime.now()
    for interval in range(0, WEATHER_FORECAST_RANGE):
        state = models.State.objects(latitude=latitude, longitude=longitude, at__lte=date).order_by('-at').first()
        precipitation = models.Precipitation.objects(latitude=latitude, longitude=longitude, date_from__lte=date, date_to__gte=date).order_by('-date_from').first()
        weather_object = {
            'at': state.at,
            'temperature': state.temperature,
            'symbol':  precipitation.symbol,
        }
        date += datetime.timedelta(days=1)
        date = date.replace(hour=FORECAST_HOUR, minute=0)
        yield weather_object

panels.panels_pool.register(WeatherPanel)