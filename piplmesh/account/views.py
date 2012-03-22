import urllib

from django import http
from django.conf import settings
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.views import generic as generic_views
from django.views.generic import simple, edit as edit_views

from piplmesh.account import forms

class RegistrationView(edit_views.FormView):
    """
    This view checks if form data are valid, saves new user.
    New user is authenticated, logged in and redirected to home page.
    """

    template_name = 'registration.html'
    form_class = forms.RegistrationForm

    # Have to do this because we don't have reverse_lazy() yet
    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        username, password = form.save()
        new_user = auth.authenticate(username=username, password=password)
        auth.login(self.request, new_user)
        super(RegistrationView, self).form_valid(self, form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return simple.redirect_to(request, url=self.get_success_url(), permanent=False)
        super(RegistrationView, self).get(self, request, *args, **kwargs)

class FacebookLoginView(generic_views.RedirectView):
    """ 
    This view authenticates the user via Facebook. 
    """

    permanent = False
    url = 'https://www.facebook.com/dialog/oauth'

    def get(self, request, *args, **kwargs):
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'scope': settings.FACEBOOK_SCOPE,
            'redirect_uri': request.build_absolute_uri(reverse('facebook_callback')),
        }
        url = self.get_redirect_url(**kwargs)
        url = "%s?%s" % (url, urllib.urlencode(args))
        if url:
            if self.permanent:
                return http.HttpResponsePermanentRedirect(url)
            else:
                return http.HttpResponseRedirect(url)
        else:
            logger.warning('Gone: %s' % self.request.path, extra={
                            'status_code': 410,
                            'request': self.request,
                        })
            return http.HttpResponseGone()
        
class FacebookLogoutView(generic_views.RedirectView):
    """ 
    Log user out of Facebook and redirect to FACEBOOK_LOGOUT_REDIRECT. 
    """

    permanent = False
    url = settings.FACEBOOK_LOGOUT_REDIRECT
    
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        super(FacebookLogoutView, self).get(self, request, *args, **kwargs)

class FacebookCallbackView(generic_views.RedirectView):
    """ 
    Authentication callback. Redirects user to LOGIN_REDIRECT_URL. 
    """

    permanent = False
    url = settings.FACEBOOK_LOGIN_REDIRECT
    
    def get(self, request, *args, **kwargs):
        token = request.GET['code']
        user = auth.authenticate(token=token, request=request)
        auth.login(request, user)
        super(FacebookCallbackView, self).get(self, request, *args, **kwargs)