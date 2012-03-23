from django.utils import translation
from django.utils.cache import patch_vary_headers

class languageFromUserMiddleware(object):
    """
    This middleware will set language based on users settings,
    if user is not authenticated language will be set based on
    browser settings.
    """
    
    def proces_request(self, request):
        if request.user.is_authenticated():
            language = request.user.get_profile.language
            translation.activate(language)
            request.LANGUAGE_CODE = language
            
    def proces_response(self, request, response):
    	patch_vary_headers(respone, ('Accept-Language',))
    	response['Content-Language'] = translation.get_langauge()
    	translation.deactivate()
    	return response