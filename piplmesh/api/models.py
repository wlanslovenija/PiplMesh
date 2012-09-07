from __future__ import absolute_import

from django.utils import timezone

import mongoengine

from pushserver.utils import updates
from piplmesh.account import models as account_models
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

    subscribers = mongoengine.ListField(mongoengine.ReferenceField(account_models.User), default=lambda: [], required=False)

    # TODO: Prevent posting comments if post is not published
    # TODO: Prevent adding attachments if post is published
    # TODO: Prevent marking post as unpublished once it was published
    is_published = mongoengine.BooleanField(default=False, required=True)

    def save(self, *args, **kwargs):
        self.updated_time = timezone.now()
        return super(Post, self).save(*args, **kwargs)

class Notification(mongoengine.Document):
    """
    This class defines document type for notifications.
    """

    recipient = mongoengine.ReferenceField(account_models.User, required=True)
    created_time = mongoengine.DateTimeField(default=lambda: timezone.now(), required=True)
    read = mongoengine.BooleanField(default=False)
    post = mongoengine.ReferenceField(Post)

    # TODO: This is probably not the best approach.
    comment = mongoengine.IntField()

    # @classmethod
    # def add_notification(cls, user, post, comment_pk):
    #     notification = cls()
    #     notification.recipient = user
    #     notification.post = post
    #     notification.comment = comment_pk
    #     notification.save()
    #     return notification

    # @classmethod
    # def notification_post_save(cls, sender, document, **kwargs):
        # if 'created' in kwargs:
            # if kwargs['created']:
                # push notification to subscriber
                # nr = api_resources.NotificationResource()
                # notification_obj = nr.obj_get(id=document.id)
                # uri = nr.get_resource_uri(notification_obj)

                # channel = "user/%s" % document.recipient.channel_id
                # updates.send_update(
                #     channel,
                #     {
                #         'type': 'notifications',
                #         'action': 'JOIN',
                #         'notifications': {
                #             'recipient': document.recipient.username,
                #             'comment': int(document.comment),
                #             'created_time': document.created_time.isoformat(),
                #             'content': document.post.comments[int(document.comment)].message,
                #             'post': str(document.post.id),
                #             'read': document.read,
                #             #'resource_uri': uri,
                #        },
                #     }
                # )

# mongoengine.signals.post_save.connect(Notification.notification_post_save, sender=Notification)

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