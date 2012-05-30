from __future__ import absolute_import

import datetime

import mongoengine

from . import base

POST_MESSAGE_MAX_LENGTH = 500
COMMENT_MESSAGE_MAX_LENGTH = 300

class Comment(base.AuthoredEmbeddedDocument):
    """
    This class defines document type for comments on posts.
    """

    message = mongoengine.StringField(max_length=COMMENT_MESSAGE_MAX_LENGTH, required=True)

class Attachment(base.AuthoredEmbeddedDocument):
    """
    This class defines document type for attachments on posts.
    """

class Post(base.AuthoredDocument):
    """
    This class defines document type for posts.
    """

    updated_time = mongoengine.DateTimeField()

    message = mongoengine.StringField(max_length=POST_MESSAGE_MAX_LENGTH, required=True)

    comments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Comment), default=lambda: [], required=False)
    attachments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Attachment), default=lambda: [], required=False)

    # TODO: Prevent posting comments if post is not published
    # TODO: Prevent adding attachments if post is published
    # TODO: Prevent marking post as unpublished once it was published
    is_published = mongoengine.BooleanField(default=False, required=True)

    def save(self, *args, **kwargs):
        self.updated_time = datetime.datetime.now()
        return super(Post, self).save(*args, **kwargs)

class UploadedFile(base.AuthoredDocument):
    """
    This class document type for uploaded files.
    """

    filename = mongoengine.StringField(required=True)
    content_type = mongoengine.StringField()

class ImageAttachment(Attachment):
    """
    This class defines document type for image attachments.
    """

    image_file = mongoengine.ReferenceField(UploadedFile, required=True)
    image_description = mongoengine.StringField(default='', required=True)

class LinkAttachment(Attachment):
    """
    This class defines document type for link attachments
    """

    link_url = mongoengine.URLField(required=True)
    link_caption = mongoengine.StringField(default='', required=True)
    link_description = mongoengine.StringField(default='', required=True)
