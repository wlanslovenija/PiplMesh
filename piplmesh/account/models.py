import uuid

from django import dispatch
from django.db import models as django_models
from django.utils import timezone

import mongoengine

from pushserver import signals

from mongo_auth.contrib import models

from .. import panels

def generate_channel_id():
    return uuid.uuid4()

class Connection(mongoengine.EmbeddedDocument):
    http_if_none_match = mongoengine.StringField()
    http_if_modified_since = mongoengine.StringField()
    channel_id = mongoengine.StringField()

class User(models.User):
    channel_id = mongoengine.UUIDField(default=generate_channel_id)

    connections = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Connection))
    connection_last_unsubscribe = mongoengine.DateTimeField()
    is_online = mongoengine.BooleanField(default=False)

    # TODO: Model for panel settings should be more semantic.
    panels_collapsed = mongoengine.DictField()
    panels_order = mongoengine.DictField()

    @django_models.permalink
    def get_absolute_url(self):
        return ('profile', (), {'username': self.username})

    def get_profile_url(self):
        return self.get_absolute_url()

    def get_panels(self):
        # TODO: Should return only panels user has enabled (should make sure users can enable panels only in the way that dependencies are satisfied)
        return panels.panels_pool.get_all_panels()

    def get_user_channel(self):
        """
        User channel is a HTTP push channel dedicated to the user. We make it private by making
        it unguessable and we cycle it regularly (every time user disconnects from all channels).
        """

        return 'user/%s' % self.channel_id

@dispatch.receiver(signals.channel_subscribe)
def process_channel_subscribe(sender, request, channel_id, **kwargs):
    request.user.update(
        push__connections={
            'http_if_none_match': request.META['HTTP_IF_NONE_MATCH'],
            'http_if_modified_since': request.META['HTTP_IF_MODIFIED_SINCE'],
            'channel_id': channel_id,
        }
    )

@dispatch.receiver(signals.channel_unsubscribe)
def process_channel_unsubscribe(sender, request, channel_id, **kwargs):
    # Importing here to prevent circular imports
    from mongo_auth import backends

    backends.User.objects(
        id=request.user.id,
        connections__http_if_none_match=request.META['HTTP_IF_NONE_MATCH'],
        connections__http_if_modified_since=request.META['HTTP_IF_MODIFIED_SINCE'],
        connections__channel_id=channel_id,
    ).update_one(unset__connections__S=1)

    request.user.update(
        pull__connections=None,
        set__connection_last_unsubscribe=timezone.now(),
    )
