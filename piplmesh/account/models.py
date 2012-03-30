from mongoengine.django import auth
import mongoengine

class User(auth.User):
    birthdate = mongoengine.DateTimeField()
    gender = mongoengine.StringField(max_length=6)
    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)