import urllib

from django import http
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.core import exceptions, urlresolvers
from django.views import generic as generic_views
from django.views.generic import simple, edit as edit_views


from django.shortcuts import render_to_response
from django.template import RequestContext
from piplmesh.account.models import User

from pushserver.utils import updates

from piplmesh.account import forms, signals


class RegistrationView(edit_views.FormView):
    """
    This view checks if form data are valid, saves new user.
    New user is authenticated, logged in and redirected to home page.
    """

    template_name = 'registration/registration.html'
    success_url = urlresolvers.reverse_lazy('home')
    form_class = forms.RegistrationForm

    def form_valid(self, form):
        username, password = form.save()
        new_user = auth.authenticate(username=username, password=password)
        auth.login(self.request, new_user)
        return super(RegistrationView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return simple.redirect_to(request, url=self.get_success_url(), permanent=False)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

class FacebookLoginView(generic_views.RedirectView):
    """ 
    This view authenticates the user via Facebook.
    """

    permanent = False

    def get_redirect_url(self, **kwargs):
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'scope': settings.FACEBOOK_SCOPE,
            'redirect_uri': self.request.build_absolute_uri(urlresolvers.reverse('facebook_callback')),
        }
        return "https://www.facebook.com/dialog/oauth?%(args)s" % {'args': urllib.urlencode(args)}

class FacebookCallbackView(generic_views.RedirectView):
    """ 
    Authentication callback. Redirects user to LOGIN_REDIRECT_URL. 
    """

    permanent = False
    # TODO: Redirect users to the page they initially came from
    url = settings.FACEBOOK_LOGIN_REDIRECT

    def get(self, request, *args, **kwargs):
        if 'code' in request.GET:
            # TODO: Add security measures to prevent attackers from sending a redirect to this url with a forged 'code'
            user = auth.authenticate(token=request.GET['code'], request=request)
            auth.login(request, user)
            return super(FacebookCallbackView, self).get(request, *args, **kwargs)
        else:
            # TODO: Message user that they have not been logged in because they cancelled the facebook app
            # TODO: Use information provided from facebook as to why the login was not successful
            return super(FacebookCallbackView, self).get(request, *args, **kwargs)

def logout(request):
    """
    After user logouts, redirect her back to the page she came from.
    """
    
    if request.method == 'POST':
        url = request.POST.get(auth.REDIRECT_FIELD_NAME)
        return auth_views.logout_then_login(request, url)
    else:
        raise exceptions.PermissionDenied




def profile(request, usrnm):
    """
    This view checks if user exist in database and returns his profile.
    """

    try:
        profile = User.objects.get(username=usrnm)
        return render_to_response('profile/profile.html',{'profile': profile}, context_instance=RequestContext(request))
    except Exception, e:
        print e
        signals.user_not_found_message(request,usrnm)
        return render_to_response('home.html', context_instance=RequestContext(request))



class SettingsView(generic_views.View):
    """
    Setings view ...
    """

    template_name = 'profile/settings.html'
    success_url = urlresolvers.reverse_lazy('home')



    def dispatch(self, request, *args, **kwargs):
        if request.user.username == kwargs["username"]:
            form = forms.UpdateForm({
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'gender': request.user.gender,
                'birthdate': request.user.birthdate,
                'avatar': "unknown.png"
            })
            return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))
        else:
            signals.no_permission_message(request)
            return render_to_response('home.html', context_instance=RequestContext(request))


