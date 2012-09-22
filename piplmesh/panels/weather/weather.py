from lxml import etree, objectify

source_url = 'http://api.met.no/'

def fetch_data(latitude, longitude):
    weather_url = '%sweatherapi/locationforecast/1.8/?lat=%s;lon=%s' % (source_url, latitude, longitude)
    parser = etree.XMLParser(remove_blank_text=True)
    lookup = objectify.ObjectifyElementClassLookup()
    parser.setElementClassLookup(lookup)
    weather = objectify.parse(weather_url, parser).getroot()
    return weather