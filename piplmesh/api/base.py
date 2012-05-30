import datetime

import mongoengine

from piplmesh.account import models

class AuthoredEmbeddedDocument(mongoengine.EmbeddedDocument):
    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now(), required=True)
    author = mongoengine.ReferenceField(models.User, required=True)

class AuthoredDocument(mongoengine.Document):
    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now(), required=True)
    author = mongoengine.ReferenceField(models.User, required=True)

    meta = {
        'abstract': True,
    }
