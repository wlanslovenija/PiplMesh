from django import dispatch
from django.contrib import messages
from django.contrib.auth import signals
from django.utils.translation import ugettext_lazy as _

def user_login_message(sender, request, user, **kwargs):
    """
    Shows success login message.
    """
    
    messages.success(request, _("You have been successfully logged in."), fail_silently=True)

signals.user_logged_in.connect(user_login_message, dispatch_uid=__name__ + '.user_login_message')

def user_logout_message(sender, request, user, **kwargs):
    """
    Shows success logout message.
    """
        
    messages.success(request, _("You have been successfully logged out."), fail_silently=True)

signals.user_logged_out.connect(user_logout_message, dispatch_uid=__name__ + '.user_logout_message')




def user_not_found_message(request,username):
    """
    Shows user not found message.
    """
    messages.success(request, _("User "+username+" not found."), fail_silently=True)

def no_permission_message(request):
    """
    Shows no permission message.
    """
    messages.success(request, _("You do not have permission to view this page."), fail_silently=True)

