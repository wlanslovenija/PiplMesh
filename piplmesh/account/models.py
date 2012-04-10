import datetime

import mongoengine
from mongoengine.django import auth
#from mongoengine import Document

from piplmesh.account import fields

LOWER_DATE_LIMIT = 366 * 120

MESSAGE_MAX_LENGTH = 500
COMMENT_MAX_LENGTH = 300

class User(auth.User):
    birthdate = fields.LimitedDateTimeField(upper_limit=datetime.datetime.today(), lower_limit=datetime.datetime.today() - datetime.timedelta(LOWER_DATE_LIMIT))
    gender = fields.GenderField()
    language = fields.LanguageField()
    
    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)

class Comment(mongoengine.EmbeddedDocument):
    """
    This class defines document type for comments on wall posts.
    """

    created_time = mongoengine.DateTimeField(default=datetime.datetime.now())
    author = mongoengine.ReferenceField(User, required=True)
    comment = mongoengine.StringField(max_length=COMMENT_MAX_LENGTH)

class Post(mongoengine.Document):
    """
    This class defines document type for posts on a wall.
    """

    author = mongoengine.ReferenceField('User', required=True)
    created_time = mongoengine.DateTimeField(default=datetime.datetime.now()) 
    updated_time = mongoengine.DateTimeField()
    comments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Comment))

class TextPost(Post):
    """
    This class defines document type for text posts.
    """

    message = mongoengine.StringField(max_length=MESSAGE_MAX_LENGTH)

class ImagePost(Post):
    """
    This class defines document type for image posts.
    """

    image_path = mongoengine.StringField()

class LinkPost(Post):
    """
    This class defines document type for link posts.
    """

    link_url = mongoengine.URLField()  
