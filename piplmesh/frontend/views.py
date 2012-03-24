from django.conf import settings
from django.views import generic as generic_views

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context.update({
            'SEARCH_ENGINE_UNIQUE_ID': settings.SEARCH_ENGINE_UNIQUE_ID,
            'SET_LANGUAGE_URL': settings.SET_LANGUAGE_URL,
        })

        return context
        
class SearchView(generic_views.TemplateView):
	template_name = 'search.html'
	
	def get_context_data(self, **kwargs):
		context = super(SearchView, self).get_context_data(**kwargs)
		
		context.update({
            'SEARCH_ENGINE_UNIQUE_ID': settings.SEARCH_ENGINE_UNIQUE_ID,
            'SET_LANGUAGE_URL': settings.SET_LANGUAGE_URL,
		})
		
		return context