from celery import task

from pushserver.utils import updates

from piplmesh.frontend import views
from . import models, stations

@task.task
def update_station_info():
    for station in stations.fetch_data():
        models.BicikeljStation.objects(station_id=station['station_id'], timestamp=station['timestamp']).update(
            set__name=station['name'],
            set__address=station['address'],
            set__location=station['location'],
            set__available=station['available'],
            set__free=station['free'],
            set__total=station['total'],
            set__open=station['open'],
            set__fetch_time=station['fetch_time'],
            upsert=True)

        # TODO: use get_or_create to know the result of the query. If created, send an update to server, otherwise just update fetch time