import datetime

import mongoengine

from piplmesh.account import models

POST_MESSAGE_MAX_LENGTH = 500
COMMENT_MESSAGE_MAX_LENGTH = 300

class AuthoredEmbeddedDocument(mongoengine.EmbeddedDocument):
    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now(), required=True)
    author = mongoengine.ReferenceField(models.User, required=True)

class AuthoredDocument(mongoengine.Document):
    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now(), required=True)
    author = mongoengine.ReferenceField(models.User, required=True)

    meta = {
        'abstract': True,
    }

class Comment(AuthoredEmbeddedDocument):
    """
    This class defines document type for comments on posts.
    """

    message = mongoengine.StringField(max_length=COMMENT_MESSAGE_MAX_LENGTH, required=True)

class Attachment(AuthoredEmbeddedDocument):
    """
    This class defines document type for attachments on posts.
    """

class Post(AuthoredDocument):
    """
    This class defines document type for posts.
    """

    updated_time = mongoengine.DateTimeField()

    message = mongoengine.StringField(max_length=POST_MESSAGE_MAX_LENGTH, required=True)

    comments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Comment), default=lambda: [], required=False)
    attachments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Attachment), default=lambda: [], required=False)

    def save(self, *args, **kwargs):
        self.updated_time = datetime.datetime.now()
        return super(Post, self).save(*args, **kwargs)

class ImageAttachment(Attachment):
    """
    This class defined document type for image attachments.
    """

    image_path = mongoengine.StringField(required=True)
    image_description = mongoengine.StringField(default='', required=True)

class LinkAttachment(Attachment):
    """
    This class defines document type for link attachments
    """

    link_url = mongoengine.URLField(required=True)
    link_caption = mongoengine.StringField(default='', required=True)
    link_description = mongoengine.StringField(default='', required=True)
