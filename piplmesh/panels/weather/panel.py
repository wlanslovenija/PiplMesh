from __future__ import absolute_import

import datetime

from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from piplmesh import nodes, panels

from . import models, weather

WEATHER_OBSOLETE = 6

class WeatherPanel(panels.BasePanel): 
    
    def get_context(self, context):

        latitude = nodes.get_node(self.request).latitude
        longitude = nodes.get_node(self.request).longitude      
        precipitation = models.Precipitation.objects(latitude=latitude, longitude=longitude).order_by('+date_to')
        state = models.State.objects(latitude=latitude, longitude=longitude).order_by('+at')
        
        if datetime.datetime.now() > state[0].created + datetime.timedelta(hours=WEATHER_OBSOLETE):
            context.update({
                'error_obsolete': True,
            })
            return context

        weather_objects = []
        for i in range(0,3):
            weather_object= {
                'at': state[i*10].at,
                'temperature':  state[i*9].temperature,
                'symbol':  precipitation[i*18].symbol
            }
            weather_objects.append(weather_object)

        context.update({
            'header': _("Weather"),
            'weather_objects': weather_objects,
            'created': state[0].created,
        })
        return context
    
panels.panels_pool.register(WeatherPanel)