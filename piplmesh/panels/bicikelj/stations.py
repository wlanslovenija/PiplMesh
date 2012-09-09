import datetime, urllib2
from xml.dom import minidom

from . import models

BICIKELJ_STATIONS_URL = 'http://www.bicikelj.si/service/carto'
BICIKELJ_INFO_URL = 'http://www.bicikelj.si/service/stationdetails/ljubljana/%d'
"""
BOUNDS_LATITUDE = map_heigth*0.703119412486786/2^(map_zoom+1)
BOUNDS_LONGITUDE = map_width*0.703119412486786/2^(map_zoom+1)
"""
BICIKELJ_BOUNDS_LATITUDE = 0.0027895
BICIKELJ_BOUNDS_LONGITUDE = 0.0027895

def get_stations_nearby(latitude, longitude):
    ids = []
    while 1:
        try:
            ids.append(models.BicikeljStation.objects(location__near= (latitude, longitude), location__within_box=((latitude-BICIKELJ_BOUNDS_LATITUDE,longitude-BICIKELJ_BOUNDS_LONGITUDE),(latitude+BICIKELJ_BOUNDS_LATITUDE,longitude+BICIKELJ_BOUNDS_LONGITUDE)), id__nin=ids).first().id)
        except:
            break
    stations = [models.BicikeljStation.objects(id=n).order_by('-timestamp').first() for n in ids]
    return stations

def fetch_data():
    stations_data = urllib2.urlopen(BICIKELJ_STATIONS_URL).read()
    stations_xml_data = minidom.parseString(stations_data)
    stations_nodes = stations_xml_data.getElementsByTagName('marker')
    info_data = [urllib2.urlopen(BICIKELJ_INFO_URL % number).read() for number in range(1,len(stations_nodes)+1)]
    info_xml_data = [minidom.parseString(info_data[i]) for i in range(len(stations_nodes))]
    data = [
        [{
            'station_id': int(stations_nodes[number].attributes['number'].value),
            'timestamp': datetime.datetime.fromtimestamp(int(info_xml_data[number].getElementsByTagName('updated')[0].firstChild.nodeValue)),
        },
        {
            'name': stations_nodes[number].attributes['name'].value,
            'address': stations_nodes[number].attributes['address'].value,
            'location': [float(stations_nodes[number].attributes['lat'].value), float(stations_nodes[number-1].attributes['lng'].value)],
            'available': int(info_xml_data[number].getElementsByTagName('available')[0].firstChild.nodeValue),
            'free': int(info_xml_data[number].getElementsByTagName('free')[0].firstChild.nodeValue),
            'total': int(info_xml_data[number].getElementsByTagName('total')[0].firstChild.nodeValue),
            'open': int(info_xml_data[number].getElementsByTagName('open')[0].firstChild.nodeValue),
        }]
        for number in range(len(stations_nodes))]
    return data