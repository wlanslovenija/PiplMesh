import datetime

from lxml import etree, objectify

import celery
from celery import task

from piplmesh import nodes
from piplmesh.utils import decorators

from . import models, panel

CHECK_FOR_NEW_WEATHER = 30 # minutes

SOURCE_URL = 'http://api.met.no/'

def fetch_data(latitude, longitude):
    """
    Get weather data for specific location
    """
    
    weather_url = '%sweatherapi/locationforecast/1.8/?lat=%s;lon=%s' % (SOURCE_URL, latitude, longitude)
    parser = etree.XMLParser(remove_blank_text=True)
    lookup = objectify.ObjectifyElementClassLookup()
    parser.setElementClassLookup(lookup)
    weather = objectify.parse(weather_url, parser).getroot()
    return weather

@task.periodic_task(run_every=datetime.timedelta(minutes=CHECK_FOR_NEW_WEATHER))
# TODO: This does not really help here as this task is short-lived (it just spawns new tasks), we should instead assure that no new subtasks are created before old ones finish
# We could lock before we create subtasks and at the end create new task which unlocks, and because of FIFO nature of the queue, unlock will happen after all subtasks
@decorators.single_instance_task()
def generate_weather_tasks():
    """
    Task which updates weather for all nodes.

    Obsolete data is currently left in the database.
    """ 
    
    weather_tasks = []
    # Fetching data only once per possible duplicate locations
    for latitude, longitude in {(node.latitude, node.longitude) for node in nodes.get_all_nodes()}:
        weather_tasks.append(update_weather.s(latitude, longitude))
    return celery.group(weather_tasks)()

# 20 tasks per second. Limitation by the api http://api.yr.no/conditions_service.html
@task.task(rate_limit=20) 
def update_weather(latitude, longitude):
    """
    Task which updates weather for one location.
    """ 
    
    weather_object = fetch_data(latitude, longitude)
    for product in weather_object.product.iterchildren():
        if datetime.datetime.strptime(product.attrib['to'], '%Y-%m-%dT%H:%M:%SZ') < datetime.datetime.strptime(weather_object.attrib['created'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(days=panel.WEATHER_FORECAST_RANGE):
            if product.attrib['from'] == product.attrib['to']:
                models.State.objects(
                    created=datetime.datetime.strptime(weather_object.attrib['created'], '%Y-%m-%dT%H:%M:%SZ'),
                    latitude=latitude, 
                    longitude=longitude,
                    model_name=weather_object.meta.model.attrib['name'],  
                    at=datetime.datetime.strptime(product.attrib['from'], '%Y-%m-%dT%H:%M:%SZ')
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
                    created=datetime.datetime.strptime(weather_object.attrib['created'], '%Y-%m-%dT%H:%M:%SZ'),
                    latitude=latitude, 
                    longitude=longitude,
                    model_name=weather_object.meta.model.attrib['name'],
                    date_from=datetime.datetime.strptime(product.attrib['from'], '%Y-%m-%dT%H:%M:%SZ'),
                    date_to=datetime.datetime.strptime(product.attrib['to'], '%Y-%m-%dT%H:%M:%SZ')
                ).update(
                    set__precipitation=product.location.precipitation.attrib['value'],
                    set__symbol=product.location.symbol.attrib['number'],
                    upsert=True
                )