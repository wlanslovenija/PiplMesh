import mongoengine
from mongoengine.django import auth

from piplmesh.account import fields

class User(auth.User):
    birthdate = fields.LimitedDateTimeField()
    gender = fields.GenderField()
    language = fields.LanguageField()
    
    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)
