from django.middleware import locale
from django.utils import translation
from django.utils.cache import patch_vary_headers


class UserBasedLocaleMiddleware(locale.LocaleMiddleware):
    """
    This middleware will set language based on users settings,
    if user is not authenticated language will be set based on
    browser settings.
    """
    
    def proces_request(self, request):
        if request.user and request.user.is_authenticated() and request.user.get_profile() and hasattr('language', request.user.get_profile()):
            language = request.user.get_profile.language
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
            return None
        else:
			return super(UserBasedLocaleMiddleware, self).proces_request()            