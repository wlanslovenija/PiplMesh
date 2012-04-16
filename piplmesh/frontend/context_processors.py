from django.conf import settings
from django.contrib import auth

def global_vars(request):
    """
    Adds global context variables to the context.
    """

    return {
        'SEARCH_ENGINE_UNIQUE_ID': settings.SEARCH_ENGINE_UNIQUE_ID,
        'LOGIN_REDIRECT_URL': settings.LOGIN_REDIRECT_URL,
        'REDIRECT_FIELD_NAME': auth.REDIRECT_FIELD_NAME,
        'redirect_to': request.REQUEST.get(auth.REDIRECT_FIELD_NAME),
    }