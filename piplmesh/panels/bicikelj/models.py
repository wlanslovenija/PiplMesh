import mongoengine

class BicikeljStation(mongoengine.Document):
    id = mongoengine.IntField(required=True)
    name = mongoengine.StringField(required=True)
    address = mongoengine.StringField(required=True)
    location = mongoengine.GeoPointField(required=True)
    open = mongoengine.IntField()
    available = mongoengine.IntField()
    free = mongoengine.IntField()
    total = mongoengine.IntField()
    timestamp = mongoengine.DateTimeField()
