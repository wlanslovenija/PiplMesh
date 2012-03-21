import urllib

from django import http
from django.conf import settings
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.views import generic as generic_views
from django.views.generic.simple import redirect_to

from piplmesh.account import forms

class RegistrationView(generic_views.TemplateView):
    """
    This view checks if form data are valid, saves new user.
    New user is authenticated, logged in and redirected to home page.
    """
    
    template_name = 'registration.html'
        
    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        form = forms.RegistrationForm()
        
        context.update({
            'search_engine': 'Google',
            'search_engine_logo': 'google_logo.png',
            'form': form
        })

        return context

    # Overridden method
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():
            return redirect_to(request, url='../', permanent=False)
        if request.method == 'POST':
            form = forms.RegistrationForm(request.POST)
            if form.is_valid():
                username, password = form.save()
                new_user = auth.authenticate(username=username, password=password)
                auth.login(request, new_user)
                return redirect_to(request, url='../', permanent=False)
        return self.render_to_response(context)
     
class FacebookLoginView(generic_views.TemplateView):
    """ 
    This view authenticates the user via Facebook. 
    """
    
    # Overridden method
    def get(self, request, *args, **kwargs):
        context = super(FacebookLoginView, self).get_context_data(**kwargs)
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'scope': settings.FACEBOOK_SCOPE,
            'redirect_uri': request.build_absolute_uri(reverse('facebook_callback')),
        }
        url_login = 'https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args)
        url_login = url_login.replace("%", "%%")
        return redirect_to(request, url=url_login, permanent=False)

class FacebookLogoutView(generic_views.TemplateView):
    """ 
    Log user out of Facebook and redirect to FACEBOOK_LOGOUT_REDIRECT. 
    """
    
    # Overridden method
    def get(self, request, *args, **kwargs):
        context = super(FacebookLogoutView, self).get_context_data(**kwargs)
        auth.logout(request)
        url_logout = (settings.FACEBOOK_LOGOUT_REDIRECT).replace("%", "%%")
        return redirect_to(request, url=url_logout, permanent=False)   

class FacebookCallbackView(generic_views.TemplateView):
    """ 
    Authentication callback. Redirects user to LOGIN_REDIRECT_URL. 
    """
    
    # Overridden method
    def get(self, request, *args, **kwargs):
        context = super(FacebookCallbackView, self).get_context_data(**kwargs)
        code = request.GET['code']
        user = auth.authenticate(token=code, request=request)
        auth.login(request, user)
        url_callback = (settings.FACEBOOK_LOGIN_REDIRECT).replace("%", "%%")
        return redirect_to(request, url=url_callback, permanent=False)