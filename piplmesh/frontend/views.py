# Create your views here.

from django.views.generic import TemplateView
from django.template import RequestContext

class MainView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context.update({
            'search_engine': 'Google',
            'search_engine_logo': 'google_logo.png'
        })
        return context