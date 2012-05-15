from django.views import generic as generic_views

from piplmesh.account import models

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['online_users'] = models.User.objects(is_online=True)
        return context
    
class SearchView(generic_views.TemplateView):
    template_name = 'search.html'