import datetime, urllib2

from lxml import objectify

from django.conf import settings
from django.utils import timezone

from . import models

BICIKELJ_STATIONS_URL = 'http://www.bicikelj.si/service/carto'
BICIKELJ_INFO_URL = 'http://www.bicikelj.si/service/stationdetails/ljubljana/%d'
POLL_BICIKELJ_INTERVAL = 60 # seconds
STALE_DATA_TIME = 10 * POLL_BICIKELJ_INTERVAL

# Formula to calculate map bounds so that we can query only stations visible on the map
#
# BOUNDS_LATITUDE and BOUNDS_LONGITUDE are the distance between a node and top location
# of the map, and the distance between a node and leftmost location of the map, respectively
# BOUNDS_LATITUDE = map_height * 0.703119412486786 / 2 ^ map_zoom
# BOUNDS_LONGITUDE = map_width * 0.703119412486786 / 2 ^ map_zoom

BICIKELJ_BOUNDS_LATITUDE = 0.00557895
BICIKELJ_BOUNDS_LONGITUDE = 0.00557895

# TODO: Check if some stations nearby have data older than STALE_DATA_TIME, then display just their names, without current state information
def get_stations_nearby(latitude, longitude):
    stations_nearby_all = models.BicikeljStation.objects(
        location__near=(latitude, longitude),
        location__within_box=((latitude - BICIKELJ_BOUNDS_LATITUDE, longitude - BICIKELJ_BOUNDS_LONGITUDE), (latitude + BICIKELJ_BOUNDS_LATITUDE, longitude + BICIKELJ_BOUNDS_LONGITUDE)),
        fetch_time__gt=timezone.now() - datetime.timedelta(seconds=STALE_DATA_TIME),
    )
    if not stations_nearby_all:
        return
    newest_station = stations_nearby_all[0]
    for station in stations_nearby_all[1:]:
        if station.station_id != newest_station.station_id:
            newest_station.old_data = newest_station.fetch_time < timezone.now() - datetime.timedelta(seconds=2 * POLL_BICIKELJ_INTERVAL)
            yield newest_station
            newest_station = station
        # timestamp changes even if there is no change in stands availability and even if there is a change
        # in stands availability, it happens that timestamp does not change, so we use also fetch time
        elif station.timestamp > newest_station.timestamp:
            newest_station = station
        elif station.timestamp == newest_station.timestamp and station.fetch_time > newest_station.fetch_time:
            newest_station = station
    newest_station.old_data = newest_station.fetch_time < timezone.now() - datetime.timedelta(seconds=2 * POLL_BICIKELJ_INTERVAL)
    yield newest_station

def fetch_data():
    stations_tree = objectify.parse(urllib2.urlopen(BICIKELJ_STATIONS_URL)).getroot()
    for node in stations_tree.markers.marker:
        info_tree = objectify.parse(urllib2.urlopen(BICIKELJ_INFO_URL % int(node.attrib['number']))).getroot()
        yield {
            'station_id': int(node.attrib['number']),
            'name': node.attrib['name'],
            'address': node.attrib['address'],
            'location': (float(node.attrib['lat']), float(node.attrib['lng'])),
            'available': int(info_tree.available),
            'free': int(info_tree.free),
            'total': int(info_tree.total),
            'open': bool(info_tree.open),
        }, datetime.datetime.utcfromtimestamp(int(info_tree.updated)), timezone.now()
