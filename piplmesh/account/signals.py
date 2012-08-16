from django import dispatch
from django.contrib import messages
from django.contrib.auth import signals
from django.utils.translation import ugettext_lazy as _

def user_login_message(sender, request, user, **kwargs):
    """
    Shows success login message.
    """
    messages.success(request, _("You have been successfully logged in."))

signals.user_logged_in.connect(user_login_message, dispatch_uid=__name__ + '.user_login_message')

def user_generate_channel_id(sender, request, user, **kwargs):
    """
    Generate new channel_id if user doesn't have one already.
    """

    if not user.channel_id:
        user.generate_channel_id()

signals.user_logged_in.connect(user_generate_channel_id, dispatch_uid=__name__ + '.user_generate_channel_id')

def user_logout_message(sender, request, user, **kwargs):
    """
    Shows success logout message.
    """
        
    messages.success(request, _("You have been successfully logged out."))

signals.user_logged_out.connect(user_logout_message, dispatch_uid=__name__ + '.user_logout_message')