from django.utils import timezone

import bson
import mongoengine

from tastypie_mongoengine import fields

from mongo_auth import backends

from . import base

POST_MESSAGE_MAX_LENGTH = 500
COMMENT_MESSAGE_MAX_LENGTH = 300

class HugRunParent(base.AuthoredEmbeddedDocument):
    """
    This class defines intermediate document type for both hugs and runs.
    """

    id = mongoengine.ObjectIdField(primary_key=True, default=lambda: bson.ObjectId())

    # So that we can access both pk and id
    pk = fields.link_property('id')

class Hug(HugRunParent):
    """
    This class defines document type for hugs.
    """

class Run(HugRunParent):
    """
    This class defines document type for runs.
    """

class Comment(base.AuthoredEmbeddedDocument):
    """
    This class defines document type for comments on posts.
    """

    id = mongoengine.ObjectIdField(primary_key=True, default=lambda: bson.ObjectId())
    message = mongoengine.StringField(max_length=COMMENT_MESSAGE_MAX_LENGTH, required=True)

    hugs = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Hug), default=lambda: [], required=False)
    hugs_count = mongoengine.IntField()
    runs = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Run), default=lambda: [], required=False)
    runs_count = mongoengine.IntField()

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

    hugs = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Hug), default=lambda: [], required=False)
    hugs_count = mongoengine.IntField()
    runs = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Run), default=lambda: [], required=False)
    runs_count = mongoengine.IntField()

    subscribers = mongoengine.ListField(mongoengine.ReferenceField(backends.User), default=lambda: [], required=False)

    # TODO: Prevent posting comments if post is not published
    # TODO: Prevent adding attachments if post is published
    # TODO: Prevent marking post as unpublished once it was published
    is_published = mongoengine.BooleanField(default=False, required=True)

    def save(self, *args, **kwargs):
        self.updated_time = timezone.now()

        self.hugs_count = len(self.hugs)
        self.runs_count = len(self.runs)

        for comment in self.comments:
            comment.hugs_count = len(comment.hugs)
            comment.runs_count = len(comment.runs)

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
    recipient = mongoengine.ReferenceField(backends.User, required=True)
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