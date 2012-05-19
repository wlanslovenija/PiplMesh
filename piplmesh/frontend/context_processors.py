from django.conf import settings
from django.contrib import auth

from piplmesh.frontend import views

def global_vars(request):
    """
    Adds global context variables to the context.
    """

    return {
        'HOME_CHANNEL_ID': views.HOME_CHANNEL_ID,
        'LOGIN_REDIRECT_URL': settings.LOGIN_REDIRECT_URL,
        'REDIRECT_FIELD_NAME': auth.REDIRECT_FIELD_NAME,
        'SEARCH_ENGINE_UNIQUE_ID': settings.SEARCH_ENGINE_UNIQUE_ID,

        'redirect_to': request.REQUEST.get(auth.REDIRECT_FIELD_NAME),
    }
