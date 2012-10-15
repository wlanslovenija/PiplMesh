import datetime

from celery import task

from . import models, stations
from piplmesh.utils import decorators

def equal(station_dict, station_object):
    for key in station_dict.keys():
        a = getattr(station_object, key)
        b = station_dict[key]
        if isinstance(a, list):
            a = tuple(a)
        if a != b:
            return False
    return True

@task.periodic_task(run_every=datetime.timedelta(seconds=stations.POLL_BICIKELJ_INTERVAL))
@decorators.single_instance_task(timeout=10 * stations.POLL_BICIKELJ_INTERVAL) # Maximum time for one task to finish is 10x the interval
def update_station_info():
    for station, timestamp, fetch_time in stations.fetch_data():
        try:
            newest_entry = models.BicikeljStation.objects(station_id=station['station_id']).order_by('-timestamp', '-fetch_time')[0]
            if equal(station, newest_entry):
                newest_entry.fetch_time = fetch_time
                newest_entry.save()
                continue
        except IndexError:
            pass

        new_entry = models.BicikeljStation.objects.create(
            timestamp=timestamp,
            fetch_time=fetch_time,
            **station
        )
        # TODO: Send an update to clients
