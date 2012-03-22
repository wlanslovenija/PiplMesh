from django.conf import settings

def global_vars(request):
    """
    Adds global context variables to the context.
    """

    return {'SEARCH_ENGINE_UNIQUE_ID': settings.SEARCH_ENGINE_UNIQUE_ID}