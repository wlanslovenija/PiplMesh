import datetime

import mongoengine
from mongoengine.django import auth

from piplmesh.account import fields

LOWER_DATE_LIMIT = 366 * 120

def upper_date_limit():
    return datetime.datetime.today()

def lower_date_limit():
    return datetime.datetime.today() - datetime.timedelta(LOWER_DATE_LIMIT)

class Connection(mongoengine.EmbeddedDocument):
    http_if_none_match = mongoengine.StringField()
    http_if_modified_since = mongoengine.StringField()
    channel_id = mongoengine.StringField()

class User(auth.User):
    birthdate = fields.LimitedDateTimeField(upper_limit=upper_date_limit, lower_limit=lower_date_limit)
    gender = fields.GenderField()
    language = fields.LanguageField()

    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)

    connections = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Connection))
    connection_last_unsubscribe = mongoengine.DateTimeField()
    is_online = mongoengine.BooleanField(default=False)
