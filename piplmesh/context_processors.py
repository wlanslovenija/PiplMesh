def search_engine(request):
    """
    Adds search engine related context variables to the context.
    """
    
    return {'search_engine': 'Google', 'search_engine_logo': 'google_logo.png'}