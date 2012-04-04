from django import dispatch
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

user_logout = dispatch.Signal(providing_args=["request", "user"])

def user_logout_message(sender, request, user, **kwargs):
    """
    Show success logout message.
    """
    
    messages.success(request, _("You have been successfully logged out."), fail_silently=True)

user_logout.connect(user_logout_message, dispatch_uid=__name__ + '.user_logout_message')