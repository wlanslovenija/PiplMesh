import urllib

from django import http
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template import context

from account import forms

def registration_view(request):
    """
    This method checks if form data are valid, saves new user.
    New user is authenticated, logged in and redirected to home page.
    """

    if request.user.is_authenticated():
        return redirect('home')
    form = forms.RegistrationForm()
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username, password = form.save()
            new_user = auth.authenticate(username=username, password=password)
            auth.login(request, new_user)
            return redirect('home')
    data = {'form': form}
    return render_to_response("registration.html", data, context_instance=context.RequestContext(request))


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