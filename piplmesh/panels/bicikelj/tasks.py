from celery import task

from pushserver.utils import updates

from piplmesh.frontend import views
from . import models, stations

@task.task
def update_station_info():
    stations_data = stations.fetch_data()
    for station in stations_data:
        station_object, created = models.BicikeljStation.objects.get_or_create(
            station_id=station[0]['station_id'],
            timestamp=station[0]['timestamp'],
            defaults = station[1]
        )
        if created:
            updates.send_update(
                views.HOME_CHANNEL_ID,
                # TODO
            )