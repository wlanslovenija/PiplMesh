import datetime

import mongoengine
from mongoengine.django import auth

from piplmesh.account import fields

# rough lower limit date
LOWER_DATE_LIMIT = 366 * 120

class User(auth.User):
    birthdate = fields.LimitedDateTimeField(upper_limit=datetime.datetime.today(), lower_limit=datetime.datetime.today() - datetime.timedelta(LOWER_DATE_LIMIT))
    gender = fields.GenderField()
    language = fields.LanguageField()
    
    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)
