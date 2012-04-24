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




def profile(request, username):
    """
    This view checks if user exist in database and returns his profile.
    """

    try:
        profile = User.objects.get(username=username)
        return render_to_response('profile/profile.html',{'profile': profile}, context_instance=RequestContext(request))
    except Exception, e:
        signals.user_not_found_message(request,username)
        return render_to_response('home.html', context_instance=RequestContext(request))




"""def settings(request, username):

    #This view checks if user has permission to access settings page


    for user in User.objects:
        if str(user) == str(username):
            if request.user.username == str(username):
                return render_to_response('profile/settings.html',{'user': request.user}, context_instance=RequestContext(request))
            else:
                signals.no_permission_message(request)
                return render_to_response('home.html', context_instance=RequestContext(request))
    signals.user_not_found_message(request,username)
    return render_to_response('home.html', context_instance=RequestContext(request))
"""



class ChangeView(edit_views.UpdateView):
    """

    """

    template_name = 'profile/settings.html'
    success_url = urlresolvers.reverse_lazy('home')
    #user = User.objects.get(username="martin")
    form_class = forms.UpdateForm2
    object = User.objects.get(username="janez")





    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """

        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
                })

        return kwargs

    def get_context_data(self, **kwargs):
        context = kwargs
        print "m"
        print self.object
        if self.object:
            context['object'] = self.object
            context_object_name = "Janez"
            if context_object_name:
                context[context_object_name] = self.object
        return context


    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return self.response_class(
            request = self.request,
            template = self.template_name,
            context = context,
            **response_kwargs
        )


