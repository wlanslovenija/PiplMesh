from django.views import generic as generic_views
from django.http import HttpResponseForbidden
from django.template import RequestContext, Context, loader
from django.conf import settings
from mongogeneric import detail
from piplmesh.account import models

HOME_CHANNEL_ID = 'home'

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['online_users'] = models.User.objects(is_online=True)
        return context

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
	
def ForbiddenView(request, reason=""):
    """
    Displays 403 fobidden page. For example, when request fails CSRF protection.
    """

    from django.middleware.csrf import REASON_NO_REFERER
    t = loader.get_template("403.html")
    return HttpResponseForbidden(t.render(RequestContext(request, {
        'DEBUG'  : settings.DEBUG,
        'reason' : reason,
        'no_referer' : reason == REASON_NO_REFERER,
    })))