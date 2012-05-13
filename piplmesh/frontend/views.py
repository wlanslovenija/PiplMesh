from django import shortcuts
from django.views import generic as generic_views

from piplmesh.account import models

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'
    
    def get_logged_in_users(self, request):
        users = models.User.objects(
            is_online = True,
        )
        return shortcuts.render_to_response(self.template_name, {'logged_in_users': users}, context_instance=RequestContext(request))
        
class SearchView(generic_views.TemplateView):
    template_name = 'search.html'