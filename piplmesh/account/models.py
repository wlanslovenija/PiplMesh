import mongoengine
from mongoengine.django import auth

from piplmesh.account import fields

class User(auth.User):
    # TODO: Add constraints
    birthdate = mongoengine.DateTimeField()
    # TODO: Add constraints
    gender = mongoengine.StringField(max_length=6)
    language = fields.LanguageField()
    
    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)
