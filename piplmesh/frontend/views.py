from django.views import generic as generic_views

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'
        
class SearchView(generic_views.TemplateView):
    template_name = 'search.html'
