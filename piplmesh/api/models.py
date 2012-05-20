import datetime

import mongoengine

from piplmesh.account import models

POST_MESSAGE_MAX_LENGTH = 500
COMMENT_MESSAGE_MAX_LENGTH = 300

class Comment(mongoengine.EmbeddedDocument):
    """
    This class defines document type for comments on posts.
    """

    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now(), required=True)
    author = mongoengine.ReferenceField(models.User, required=True)
    message = mongoengine.StringField(max_length=COMMENT_MESSAGE_MAX_LENGTH, required=True)

class Attachment(mongoengine.EmbeddedDocument):
    """
    This class defines document type for attachments on posts.
    """

    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now(), required=True)
    author = mongoengine.ReferenceField(models.User, required=True)

class Post(mongoengine.Document):
    """
    This class defines document type for posts.
    """

    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now(), required=True)
    updated_time = mongoengine.DateTimeField(required=True)
    author = mongoengine.ReferenceField(models.User, required=True)

    message = mongoengine.StringField(max_length=POST_MESSAGE_MAX_LENGTH, required=True)

    comments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Comment), default=lambda: [], required=False)
    attachments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Attachment), default=lambda: [], required=False)

class ImageAttachment(Attachment):
    """
    This class defined document type for image attachments.
    """

    image_path = mongoengine.StringField(required=True)
    image_description = mongoengine.StringField(default='')

class LinkAttachment(Attachment):
    """
    This class defines document type for link attachments
    """

    link_url = mongoengine.URLField(required=True)
    link_caption = mongoengine.StringField(default='')
    link_description = mongoengine.StringField(default='')
