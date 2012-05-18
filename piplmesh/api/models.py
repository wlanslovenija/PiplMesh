import datetime

import mongoengine

from piplmesh.account import models

POST_MESSAGE_MAX_LENGTH = 500
COMMENT_MESSAGE_MAX_LENGTH = 300

class Comment(mongoengine.EmbeddedDocument):
    """
    This class defines document type for comments on wall posts.
    """

    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now())
    author = mongoengine.ReferenceField(models.User, required=True)
    message = mongoengine.StringField(max_length=COMMENT_MESSAGE_MAX_LENGTH)

class Post(mongoengine.Document):
    """
    This class defines document type for posts on a wall.
    """

    author = mongoengine.ReferenceField(models.User, required=True)
    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now())
    updated_time = mongoengine.DateTimeField()
    comments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Comment))

    meta = {
        'allow_inheritance': True,
    }

class TextPost(Post):
    """
    This class defines document type for text posts.
    """

    message = mongoengine.StringField(max_length=POST_MESSAGE_MAX_LENGTH)

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
    link_caption = mongoengine.StringField()
    link_description = mongoengine.StringField()
