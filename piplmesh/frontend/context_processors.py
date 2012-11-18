from django.conf import settings
from django.utils import translation

from piplmesh import urls
from piplmesh.frontend import forms, tasks

def global_vars(request):
    """
    Adds global context variables to the context.
    """
    context = {
        # Constants
        'HOME_CHANNEL_ID': tasks.HOME_CHANNEL_ID,
        'SEARCH_ENGINE_UNIQUE_ID': settings.SEARCH_ENGINE_UNIQUE_ID,
        'API_NAME': urls.API_NAME,

        # Variables
        'logo_url': "piplmesh/images/logo-%s.png" % translation.get_language(),
    }

    # Location
    if getattr(request, 'user', None) and request.user.is_authenticated() and request.user.is_staff:
        context.update({
            'location_form': forms.LocationForm(initial={'location': forms.initial_location(request)}),
        })

    return context
