import datetime

import mongoengine
from mongoengine.django import auth

from piplmesh.account import fields

class User(auth.User):
    birthdate = fields.LimitedDateTimeField(upper_limit=datetime.datetime.today())
    gender = fields.GenderField()
    language = fields.LanguageField()
    
    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)
