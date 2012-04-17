import datetime

from celery.task import task

from pushserver.utils import updates

from piplmesh.account import models

@task
def prune_users():
    chan_users = models.User.objects()
    for user in chan_users:
        # TODO: Implement joining/parting subsystem
        channel_id = 'a'

        if len(user.connections) == 0 and user.connection_last_unsubscribe and datetime.datetime.now() > user.connection_last_unsubscribe + datetime.timedelta(seconds=30):
            user.update(
                set__connections=[],
                unset__connection_last_unsubscribe=1,
                set__is_online=False,
            )

            updates.send_update(
                channel_id,
                {
                    'type': 'userlist',
                    'action': 'PART',
                    'username': user.username,
                }
            )
        elif len(user.connections) > 0 and user.is_online == False:
            user.update(
                set__is_online=True,
            )

            updates.send_update(
                channel_id,
                {
                    'type': 'userlist',
                    'action': 'JOIN',
                    'username': user.username,
                }
            )