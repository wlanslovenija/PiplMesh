import urllib2
from datetime import date, datetime, timedelta
from lxml import etree, objectify
from pytz import UTC

from piplmesh import settings
from . import models

BICIKELJ_STATIONS_URL = 'http://www.bicikelj.si/service/carto'
BICIKELJ_INFO_URL = 'http://www.bicikelj.si/service/stationdetails/ljubljana/%d'

""" A comment explaining how to calculate map bounds, so we can search for stations visible on map only

BOUNDS_LATITUDE and BOUNDS_LONGITUDE are the distance between a node and top location of the map
and the distance between a node and leftmost location of the map, respectively
BOUNDS_LATITUDE = map_heigth*0.703119412486786/2^map_zoom
BOUNDS_LONGITUDE = map_width*0.703119412486786/2^map_zoom

"""

BICIKELJ_BOUNDS_LATITUDE = 0.00557895
BICIKELJ_BOUNDS_LONGITUDE = 0.00557895

def get_stations_nearby(latitude, longitude):
    stations_nearby_all = models.BicikeljStation.objects(
                location__near=(latitude, longitude),
                location__within_box=((latitude-BICIKELJ_BOUNDS_LATITUDE,longitude-BICIKELJ_BOUNDS_LONGITUDE),(latitude+BICIKELJ_BOUNDS_LATITUDE,longitude+BICIKELJ_BOUNDS_LONGITUDE)),
                fetch_time__gt=datetime.now() - timedelta(seconds=12*settings.POLL_BICIKELJ_INTERVAL),
    )
    n = stations_nearby_all[0].station_id
    station_idx = []
    for j,station in enumerate(stations_nearby_all):
        if station.station_id != n:
            station_idx.append(j-1)
            n = station.station_id
    station_idx.append(len(stations_nearby_all)-1)
    stations_nearby = [stations_nearby_all[i] for i in station_idx]
    for station in stations_nearby:
        station.old_data = station.fetch_time < UTC.localize(datetime.now() - timedelta(seconds=2*settings.POLL_BICIKELJ_INTERVAL))
        station.very_old_data = station.fetch_time < UTC.localize(datetime.now() - timedelta(seconds=10*settings.POLL_BICIKELJ_INTERVAL))
    return stations_nearby

def fetch_data():
    stations_tree = objectify.fromstring(urllib2.urlopen(BICIKELJ_STATIONS_URL).read())
    data = []
    for node in stations_tree.markers.marker:
        info_data = objectify.fromstring(urllib2.urlopen(BICIKELJ_INFO_URL % int(node.attrib['number'])).read())
        data.append(
            {
                'station_id': int(node.attrib['number']),
                'timestamp': datetime.fromtimestamp(int(info_data.updated)),
                'name': node.attrib['name'],
                'address': node.attrib['address'],
                'location': (float(node.attrib['lat']), float(node.attrib['lng'])),
                'available': int(info_data.available),
                'free': int(info_data.free),
                'total': int(info_data.total),
                'open': bool(info_data.open),
                'fetch_time': datetime.now(),
            }
        )
    return data