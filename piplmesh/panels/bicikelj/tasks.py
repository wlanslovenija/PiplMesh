from celery import task

from pushserver.utils import updates

from piplmesh.frontend import views
from . import models, stations

@task.task
def update_station_info():
    station_info = stations.fetch_data()
    for station in station_info:
        print station['id']
        print station
        if not models.BicikeljStation.objects(id=station['id'], timestamp=station['timestamp']):
            models.BicikeljStation(
                                   name=station['name'],
                                   address=station['address'],
                                   id=station['id'],
                                   location=station['location'],
                                   timestamp=station['timestamp'],
                                   available = station['available'],
                                   free = station['free'],
                                   total = station['total'],
                                   open = station['open'],
            ).save()
            updates.send_update(
                views.HOME_CHANNEL_ID,
                # TODO
                )