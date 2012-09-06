import datetime

from django.conf import settings
from django.utils import timezone

from celery import task

from pushserver.utils import updates

from piplmesh.account import models
from piplmesh.frontend import views

CHECK_ONLINE_USERS_RECONNECT_TIMEOUT = 2 * settings.CHECK_ONLINE_USERS_INTERVAL

@task.task
def check_online_users():
    for user in models.User.objects(
        is_online=False,
        connections__not__in=([], None), # None if field is missing altogether, not__in seems not to be equal to nin
    ):
        if models.User.objects(
            pk=user.pk,
            is_online=False,
            connections__not__in=([], None), # None if field is missing altogether, not__in seems not to be equal to nin
        ).update(set__is_online=True):
            updates.send_update(
                views.HOME_CHANNEL_ID,
                {
                    'type': 'user_connect',
                    'user': {
                        'username': user.username,
                        'profile_url': user.get_profile_url(),
                        'image_url': user.get_image_url(),
                    },
                }
            )

    for user in models.User.objects(
        is_online=True,
        connections__in=([], None), # None if field is missing altogether
        connection_last_unsubscribe__lt=timezone.now() - datetime.timedelta(seconds=CHECK_ONLINE_USERS_RECONNECT_TIMEOUT),
    ):
        if models.User.objects(
            pk=user.pk,
            is_online=True,
            connections__in=([], None), # None if field is missing altogether
            connection_last_unsubscribe__lt=timezone.now() - datetime.timedelta(seconds=CHECK_ONLINE_USERS_RECONNECT_TIMEOUT),
        ).update(set__is_online=False):
            updates.send_update(
                views.HOME_CHANNEL_ID,
                {
                    'type': 'user_disconnect',
                    'user': {
                        'username': user.username,
                        'profile_url': user.get_absolute_url(),
                        'image_url': user.get_image_url(),
                    },
                }
            )
