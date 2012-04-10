import datetime

import mongoengine
from mongoengine.django import auth
#from mongoengine import Document

from piplmesh.account import fields

LOWER_DATE_LIMIT = 366 * 120

TEXT_POST_MAX_LENGTH = 500
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
    This class defines document type for storing post on our wall.
    """

    author = mongoengine.ReferenceField('User', required=True)
    created_time = mongoengine.DateTimeField(default=datetime.datetime.now()) 
    edited_time = mongoengine.DateTimeField()
    comments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Comment))

class TextPost(Post):
    """
    This class defines support for posting text in wall posts.
    """

    text = mongoengine.StringField(max_length=TEXT_POST_MAX_LENGTH)

class ImagePost(Post):
    """
    This class defines support for posting images in wall posts.
    """

    image_path = mongoengine.StringField()

class LinkPost(Post):
    """
    This class defines support for posting links in wall posts.
    """

    link_url = mongoengine.URLField()  
