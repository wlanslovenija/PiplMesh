from django import http, template 
from django.conf import settings
from django.views import generic as generic_views

from mongogeneric import detail

from piplmesh.account import models

HOME_CHANNEL_ID = 'home'

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['online_users'] = models.User.objects(is_online=True)
        return context

# TODO: Get HTML5 geolocation data and store it into request session
class OutsideView(generic_views.TemplateView):
    template_name = 'outside.html'

class SearchView(generic_views.TemplateView):
    template_name = 'search.html'

class UserView(detail.DetailView):
    """
    This view checks if user exist in database and returns his user page (profile).
    """

    template_name = 'user/user.html'
    document = models.User
    slug_field = 'username'
    slug_url_kwarg = 'username'
	
def forbidden_view(request, reason=''):
    """
    Displays 403 fobidden page. For example, when request fails CSRF protection.
    """

    from django.middleware import csrf
    t = template.loader.get_template('403.html')
    return http.HttpResponseForbidden(t.render(template.RequestContext(request, {
        'DEBUG': settings.DEBUG,
        'reason': reason,
        'no_referer': reason == csrf.REASON_NO_REFERER,
    })))