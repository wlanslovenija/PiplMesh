import datetime

from django.conf import settings

from celery.task import task

from pushserver.utils import updates

from piplmesh.account import models

CHECK_ONLINE_USERS_RECONNECT_TIMEOUT = 2 * settings.CHECK_ONLINE_USERS_INTERVAL

@task
def check_online_users():
    for user in models.User.objects():
        channel_id = 'a'
        if models.User.objects( \
            id=user.id, \
            is_online=True, \
            connections=[], \
            connection_last_unsubscribe__lt=datetime.datetime.now() - datetime.timedelta(seconds=CHECK_ONLINE_USERS_RECONNECT_TIMEOUT), \
        ).update(set__is_online=False):
            updates.send_update(
                channel_id,
                {
                    'type': 'userlist',
                    'action': 'PART',
                    'username': user.username,
                }
            )
        elif models.User.objects( \
            id=user.id, \
            is_online=False, \
            connections__ne=[], \
        ).update(set__is_online=True):
            updates.send_update(
                channel_id,
                {
                    'type': 'userlist',
                    'action': 'JOIN',
                    'username': user.username,
                }
            )