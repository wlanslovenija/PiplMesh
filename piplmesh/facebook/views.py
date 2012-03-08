import urllib

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django import http

def facebook_login(request):
    """ 
    Authenticate user via Facebook. 
    """
    
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri(reverse('facebook_callback')),
    }
    url = 'https://www.facebook.com/dialog/oauth?'
    return http.HttpResponseRedirect('%s%s' % (url, urllib.urlencode(args)))

def facebook_logout(request):
    """ 
    Log user out of Facebook and redirect to FACEBOOK_LOGOUT_REDIRECT. 
    """
    
    logout(request)
    return http.HttpResponseRedirect(settings.FACEBOOK_LOGOUT_REDIRECT)

def facebook_callback(request):
    """ 
    Authentication callback. Redirects user to LOGIN_REDIRECT_URL. 
    """
    
    code = request.GET['code']
    user = authenticate(token=code, request=request)
    login(request, user)
    return http.HttpResponseRedirect(settings.FACEBOOK_LOGIN_REDIRECT)