from __future__ import absolute_import

from celery import task
from datetime import datetime
from lxml import etree, objectify

from piplmesh import nodes

from . import models

source_url = 'http://api.met.no/'

def fetch_data(latitude, longitude):
    weather_url = '%sweatherapi/locationforecast/1.8/?lat=%s;lon=%s' % (source_url, latitude, longitude)
    parser = etree.XMLParser(remove_blank_text=True)
    lookup = objectify.ObjectifyElementClassLookup()
    parser.setElementClassLookup(lookup)
    weather = objectify.parse(weather_url,parser).getroot()
    return weather

@task.task
def update_weather():
    """
    Task which updates weather for all nodes.

    Obsolete data is currently left in the database.
    """
    
    for node in nodes.get_all_nodes():   
        weather_object = fetch_data(node.latitude, node.longitude)
        for product in weather_object.product.iterchildren():
            if product.attrib['from'] == product.attrib['to']:
                models.State.objects(
                    created=datetime.strptime(weather_object.attrib['created'], '%Y-%m-%dT%H:%M:%SZ'),
                    latitude=node.latitude, 
                    longitude=node.longitude,
                    model_name=weather_object.meta.model.attrib['name'],  
                    at=datetime.strptime(product.attrib['from'], '%Y-%m-%dT%H:%M:%SZ')
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
                    created=datetime.strptime(weather_object.attrib['created'], '%Y-%m-%dT%H:%M:%SZ'),
                    latitude=node.latitude, 
                    longitude=node.longitude,
                    model_name=weather_object.meta.model.attrib['name'],
                    date_from=datetime.strptime(product.attrib['from'], '%Y-%m-%dT%H:%M:%SZ'),
                    date_to=datetime.strptime(product.attrib['to'], '%Y-%m-%dT%H:%M:%SZ')
                ).update(
                    set__precipitation=product.location.precipitation.attrib['value'],
                    set__symbol=product.location.symbol.attrib['number'],
                    upsert=True
                )