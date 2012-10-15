from django.utils import timezone

import bson
import mongoengine

from tastypie_mongoengine import fields

from . import base
from piplmesh.account import models as account_models

POST_MESSAGE_MAX_LENGTH = 500
COMMENT_MESSAGE_MAX_LENGTH = 300

class Comment(base.AuthoredEmbeddedDocument):
    """
    This class defines document type for comments on posts.
    """

    id = mongoengine.ObjectIdField(primary_key=True, default=lambda: bson.ObjectId())
    message = mongoengine.StringField(max_length=COMMENT_MESSAGE_MAX_LENGTH, required=True)

    # So that we can access both pk and id
    pk = fields.link_property('id')

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

    subscribers = mongoengine.ListField(mongoengine.ReferenceField(account_models.User), default=lambda: [], required=False)

    # TODO: Prevent posting comments if post is not published
    # TODO: Prevent adding attachments if post is published
    # TODO: Prevent marking post as unpublished once it was published
    is_published = mongoengine.BooleanField(default=False, required=True)

    def save(self, *args, **kwargs):
        self.updated_time = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def get_comment(self, comment_pk):
        # TODO: Would it be faster to traverse in reversed direction? Because probably last comments are fetched more often in practice?
        # TODO: Should we cache information about mappings between IDs and comments?
        for comment in self.comments:
            if comment.pk == comment_pk:
                return comment

        raise IndexError("Comment with primary key '%s' not found in post '%s'." % (comment_pk, self.pk))

class Notification(mongoengine.Document):
    """
    This class defines document type for notifications.
    """

    created_time = mongoengine.DateTimeField(required=True)
    recipient = mongoengine.ReferenceField(account_models.User, required=True)
    read = mongoengine.BooleanField(default=False)
    post = mongoengine.ReferenceField(Post)
    comment = mongoengine.ObjectIdField()

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