from django.contrib import auth
from django.contrib.auth import models as auth_models
from django.middleware import locale
from django.utils import translation

from piplmesh.account import models

class UserBasedLocaleMiddleware(locale.LocaleMiddleware):
    """
    This middleware will set language based on users settings,
    if user is not authenticated language will be set based on
    browser settings.
    """

    # TODO: This should be converted to MongoEngine and renamed without TODO prefix
    def TODO_process_request(self, request):
        if request.user and request.user.is_authenticated() and request.user.get_profile() and hasattr('language', request.user.get_profile()):
            language = request.user.get_profile.language
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
            return None
        else:
            return super(UserBasedLocaleMiddleware, self).proces_request()

class LazyUserMiddleware(object):
    def process_request(self, request):
        if request.user and not isinstance(request.user, auth_models.AnonymousUser):
            assert isinstance(request.user, models.User)
            return None

        user = auth.authenticate()
        assert user.is_anonymous()

        # We set the auth session key to prevent login to
        # cycle the session key or flush the whole session
        request.session[auth.SESSION_KEY] = user.id

        auth.login(request, user)

        return None
