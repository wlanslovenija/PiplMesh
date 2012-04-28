import datetime

from django.conf import settings

from celery import task

from pushserver.utils import updates

from piplmesh.account import models
from piplmesh.frontend import views

CHECK_ONLINE_USERS_RECONNECT_TIMEOUT = 2 * settings.CHECK_ONLINE_USERS_INTERVAL

@task.task
def check_online_users():
    # TODO: Iterating over all users in Python could become really slow once there are millions of users, much better is to limit the query only to potentially interesting users (conditions are already bellow)
    for user in models.User.objects():
        if models.User.objects(
            id=user.id,
            is_online=True,
            connections=[],
            connection_last_unsubscribe__lt=datetime.datetime.now() - datetime.timedelta(seconds=CHECK_ONLINE_USERS_RECONNECT_TIMEOUT),
        ).update(set__is_online=False):
            updates.send_update(
                views.HOME_CHANNEL_ID,
                {
                    'type': 'userlist',
                    'action': 'PART',
                    'username': user.username,
                }
            )
        elif models.User.objects(
            id=user.id,
            is_online=False,
            connections__ne=[],
        ).update(set__is_online=True):
            updates.send_update(
                views.HOME_CHANNEL_ID,
                {
                    'type': 'userlist',
                    'action': 'JOIN',
                    'username': user.username,
                }
            )
