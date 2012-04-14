from django import http
from django.conf import settings
from django.utils import functional

from piplmesh.account import utils

def facebook_required(view):
    """
    Facebook login required decorator.

    Checks to see if user's access token is valid. If not, the user is
    redirected to the URL specified in FACEBOOK_ERROR_REDIRECT. This is a layer
    of protection for Facebook-dependent pages. The user remains authenticated
    until logging out.
    """
  
    @functional.wraps(view)
    def inner(request, *args, **kwargs):
        url = getattr(settings, 'FACEBOOK_ERROR_REDIRECT', '/')
        if request.user.is_authenticated():
            if utils.valid_token(request.user):
                pass
            else:
                return http.HttpResponseRedirect(url)
        else:
            return http.HttpResponseRedirect(url)
        return view(request, *args, **kwargs)
    
    return inner