from django.views import generic as generic_views

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context.update({
            'search_engine': 'Google',
            'search_engine_logo': 'google_logo.png'
        })

        return context
        