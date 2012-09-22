from __future__ import absolute_import

from celery import task
from datetime import datetime

from piplmesh import nodes

from . import models, weather as weather_functions

@task.task
def update_weather():
    """
    Task which updates weather for all nodes.

    Obsolete data is currently left in the database.
    """
    
    for node in nodes.get_all_nodes():   
        weather_object = weather_functions.fetch_data(node.latitude, node.longitude)
        for product in weather_object.product.iterchildren():
            DATE_FROM = datetime.strptime(product.attrib['from'], "%Y-%m-%dT%H:%M:%SZ")
            DATE_TO = datetime.strptime(product.attrib['to'], "%Y-%m-%dT%H:%M:%SZ")
            if DATE_FROM == DATE_TO:
                models.State.objects(
                    created=datetime.strptime(weather_object.attrib['created'], "%Y-%m-%dT%H:%M:%SZ"),
                    latitude=node.latitude, 
                    longitude=node.longitude,
                    model_name=weather_object.meta.model.attrib['name'],  
                    at=DATE_FROM
                ).update(
                    set__temperature=product.location.temperature.attrib['value'],
                    set__wind_direction=product.location.windDirection.attrib['name'],
                    set__wind_angle=product.location.windDirection.attrib['deg'],
                    set__wind_speed=product.location.windSpeed.attrib['mps'],
                    set__humidity=product.location.humidity.attrib['value'],
                    set__pressure=product.location.pressure.attrib['value'],
                    set__cloudiness=product.location.cloudiness.attrib['percent'],
                    set__fog=product.location.fog.attrib['percent'],
                    set__low_clouds=product.location.lowClouds.attrib['percent'],
                    set__medium_clouds=product.location.mediumClouds.attrib['percent'],
                    set__high_clouds=product.location.highClouds.attrib['percent'],
                    upsert=True
                )
            else:
                models.Precipitation.objects(
                    created=datetime.strptime(weather_object.attrib['created'], "%Y-%m-%dT%H:%M:%SZ"),
                    latitude=node.latitude, 
                    longitude=node.longitude,
                    model_name=weather_object.meta.model.attrib['name'],
                    date_from=DATE_FROM,
                    date_to=DATE_TO
                ).update(
                    set__precipitation=product.location.precipitation.attrib['value'],
                    set__symbol=product.location.symbol.attrib['number'],
                    upsert=True
                )