from django.utils import timezone

import mongoengine

from mongo_auth import backends

class AuthoredEmbeddedDocument(mongoengine.EmbeddedDocument):
    created_time = mongoengine.DateTimeField(default=lambda: timezone.now(), required=True)
    author = mongoengine.ReferenceField(backends.User, required=True)

class AuthoredDocument(mongoengine.Document):
    created_time = mongoengine.DateTimeField(default=lambda: timezone.now(), required=True)
    author = mongoengine.ReferenceField(backends.User, required=True)

    meta = {
        'abstract': True,
    }
