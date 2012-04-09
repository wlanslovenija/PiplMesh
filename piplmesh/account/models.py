import datetime

import mongoengine
from mongoengine.django import auth

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

class Post(mongoengine.Document):
    """
    This class defines document type for storing post on our wall.
    """

    author = mongoengine.ReferenceField('User', required=True)
    created_time = fields.DateTimeField(auto_now_add=True) 
    edited_time = fields.DateTimeField()
    comments = fields.ListFields(EmbeddedDocumentField(Comment))

class TextPost(Post):
    """
    This class defines support for posting text in wall posts.
    """

    text = fields.StringField(max_langth=TEXT_POST_MAX_LENGTH)

class ImagePost(Post):
    """
    This class defines support for posting images in wall posts.
    """

    image_path = fields.StringField()

class LinkPost(Post):
    """
    This class defines support for posting links in wall posts.
    """

    link_url = fields.URLField()  

class Comment(mongoengine.EmbeddedDocument):
    """
    This class defines document type for comments on wall posts.
    """

    created_time = fields.DateTimeField(auto_now_add=True)
    author = fields.ReferencedField(User, required=True)
    comment = fields.StringField(max_length=COMMENT_MAX_LENGTH)
