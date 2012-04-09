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

    author = fields.ReferenceField(User, required=True, reverese_delete_rule=CASCADE)
    created_time = fields.DateTimeField(auto_now_add=True) 
    edited_time = fields.DateTimeField()

class TextPost(Post):
    """
    This class adds support for posting text in wall posts.
    """

    message = fields.StringField(max_langth=MAX_USER_POST_MESSAGE_LENGTH)

class ImagePost(Post):
    """
    This class adds support for posting images in wall posts. For now we don't support uploading photos.
    """

    image_path = fields.StringField()

class LinkPost(Post):
    """
    This class adds support for posting links in wall posts.
    """

    link_url = fields.URLField()

class PostComments(Post):
    """
    Adds support for storing comments under each post.
    """

    comments = fields.ListFields(EmbeddedDocumentField(Comment))

class Comment(mongoengine.EmbeddedDocument):
    """
    This class defines embedded Document type for comments on wall posts. .
    """

    created_time = fields.DateTimeField(auto_now_add=True)
    author = fields.ReferencedField(User, required=True)
    text = fields.StringField(max_length = COMMENT_MAX_LENGTH)
