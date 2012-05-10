import datetime, urllib

from django import dispatch, http, shortcuts, template
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.core import exceptions, urlresolvers
from django.views import generic as generic_views
from django.views.generic import simple, edit as edit_views

from pushserver import signals
from pushserver.utils import updates

from piplmesh.account import forms, models

HOME_CHANNEL_ID = 'home'

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

@dispatch.receiver(signals.channel_subscribe)
def process_channel_subscribe(sender, request, channel_id, **kwargs):
    request.user.update(
        push__connections={
            'http_if_none_match': request.META['HTTP_IF_NONE_MATCH'],
            'http_if_modified_since': request.META['HTTP_IF_MODIFIED_SINCE'],
            'channel_id': channel_id,
        }
    )

@dispatch.receiver(signals.channel_unsubscribe)
def process_channel_unsubscribe(sender, request, channel_id, **kwargs):
    models.User.objects(
        id=request.user.id,
        connections__http_if_none_match=request.META['HTTP_IF_NONE_MATCH'],
        connections__http_if_modified_since=request.META['HTTP_IF_MODIFIED_SINCE'],
        connections__channel_id=channel_id,
    ).update_one(unset__connections__S=1)

    request.user.update(
        pull__connections=None,
        set__connection_last_unsubscribe=datetime.datetime.now(),
    )

class ProfileView(generic_views.View):
    """
    This view checks if user exist in database and returns his profile.
    """

    template_name = 'profile/profile.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            profile = models.User.objects.get(username=kwargs['username'])
            return shortcuts.render_to_response(self.template_name,{'profile': profile}, context_instance=template.RequestContext(request))
        except Exception, e:
            message = "User "+kwargs['username']+" not found."
            messages.error(request,message)
            # TODO: Redirect user to page where he came from
            return shortcuts.render_to_response('home.html', context_instance=template.RequestContext(request))

class SettingsView(edit_views.FormView):
    """
    This view displays form for updating user settings. It checks if all fields are valid and updates user.
    It also prevents unauthorised access to user settings page.
    """

    template_name = 'profile/settings.html'
    form_class = forms.UpdateForm
    user = models.User

    def form_valid(self, form):
        if self.user.check_password(form.cleaned_data['old_password']):
            self.user.first_name=form.cleaned_data['first_name']
            self.user.last_name=form.cleaned_data['last_name']
            self.user.email=form.cleaned_data['email']
            self.user.gender=form.cleaned_data['gender']
            self.user.birthdate=form.cleaned_data['birthdate']
            # TODO: Change user image
            profile_image = form.cleaned_data['profile_image']
            self.user.save()
            if form.cleaned_data['new_password1']:
                if form.cleaned_data['new_password1'] == form.cleaned_data['new_password2']:
                    self.user.set_password(form.cleaned_data['new_password1'])
                else:
                    messages.error(self.request,"Passwords do not match")
                    return super(SettingsView, self).form_invalid(form)
            messages.error(self.request,"You have successfully modified your settings")
            return super(SettingsView, self).form_valid(form)
        else:
            messages.error(self.request,"You have entered invalid password")
            return super(SettingsView, self).form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.username == kwargs["username"]:
            self.success_url = urlresolvers.reverse_lazy('profile', kwargs={'username': request.user.username})
            if request.user.facebook_id:
                # TODO: Settings for users with Facebook login
                messages.error(request,"Settings for users with Facebook login are not available at this moment")
                return shortcuts.redirect(self.success_url)
            self.user = models.User.objects.get(username=request.user.username)
            self.initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'gender': request.user.gender,
                'birthdate': request.user.birthdate,
                # TODO: Path to user current avatar
                'profile_image': "unknown.png"
            }
            return super(SettingsView, self).dispatch(request, *args, **kwargs)
        else:
            messages.error(request,"You do not have permission to view this page.")
            # TODO: Redirect user to page where he came from
            return shortcuts.render_to_response('home.html', context_instance=template.RequestContext(request))
