import mongoengine

class BicikeljStation(mongoengine.Document):
    station_id = mongoengine.IntField(required=True, unique_with='timestamp')
    timestamp = mongoengine.DateTimeField(required=True, unique_with='station_id')
    fetch_time = mongoengine.DateTimeField(required=True)
    name = mongoengine.StringField(required=True)
    address = mongoengine.StringField(required=True)
    location = mongoengine.GeoPointField(required=True)
    open = mongoengine.BooleanField(required=True)
    available = mongoengine.IntField(required=True)
    free = mongoengine.IntField(required=True)
    total = mongoengine.IntField(required=True)

    meta = {
        'indexes': ['station_id', 'timestamp'],
    }
