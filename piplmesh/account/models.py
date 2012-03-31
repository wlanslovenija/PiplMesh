import mongoengine
from mongoengine.django import auth

from piplmesh.account import fields

class User(auth.User):
    # TODO: Add birthdate constraints
    birthdate = mongoengine.DateTimeField()
    gender = fields.GenderField()
    language = fields.LanguageField()
    
    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)
