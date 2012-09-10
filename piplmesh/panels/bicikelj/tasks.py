from celery import task

from pushserver.utils import updates

from piplmesh.frontend import views
from . import models, stations

@task.task
def update_station_info():
    for station in stations.fetch_data():
        station_object, created = models.BicikeljStation.objects.get_or_create(
            station_id=station['station_id'],
            timestamp=station['timestamp'],
            defaults=station,
        )
        # TODO: if created, send an update to server