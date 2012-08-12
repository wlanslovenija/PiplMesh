from django.dispatch import receiver

from pushserver.utils import updates

from piplmesh.api import signals as api_signals
from piplmesh.frontend import views

@receiver(api_signals.post_created)
def handle_post_created(sender, **kwargs):
    if kwargs.get("post_published"):
        updates.send_update(
            views.HOME_CHANNEL_ID,
                {
                'type': 'posts',
                'action': 'NEW',
                'post': {
                    'location': kwargs.get("post_location"),
                    },
                }
        )