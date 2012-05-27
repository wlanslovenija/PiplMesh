import json, urlparse, urllib

from django.conf import settings
from django.core import urlresolvers

from mongoengine.django import auth

import tweepy

from piplmesh.account import models

class MongoEngineBackend(auth.MongoEngineBackend):
    # TODO: Implement object permission support
    supports_object_permissions = False
    # TODO: Implement anonymous user backend
    supports_anonymous_user = False
    # TODO: Implement inactive user backend
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        user = self.user_class.objects(username__iexact=username).first()
        if user:
            if password and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.with_id(user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        return models.User

class FacebookBackend(MongoEngineBackend):
    """
    Facebook authentication.
    """

    def authenticate(self, facebook_token=None, request=None):
        """
        Retrieves an access token and Facebook data. Determine if user already
        exists. If not, a new user is created. Finally, the user's Facebook
        data is saved.
        """
    
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': request.build_absolute_uri(urlresolvers.reverse('facebook_callback')),
            'code': facebook_token,
        }
    
        # Retrieve access token
        url = urllib.urlopen('https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode(args)).read()
        response = urlparse.parse_qs(url)
        access_token = response['access_token'][-1]
    
        # Retrieve user's public profile information
        data = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % access_token)
        fb = json.load(data)

        # TODO: Check if id and other fields are returned
        # TODO: Move user retrieval/creation to User document/manager
        # TODO: get_or_create implementation has in fact a race condition, is this a problem?
        user, created = self.user_class.objects.get_or_create(
            facebook_id=fb.get('id'),
            defaults={
                'username': fb.get('username', fb.get('first_name') + fb.get('last_name')),
                'first_name': fb.get('first_name'),
                'last_name': fb.get('last_name'),
                'email': fb.get('email'),
                'gender': fb.get('gender'),
                'facebook_link': fb.get('link'),
            }
        )
        user.facebook_token = access_token
        user.save()

        return user

class TwitterBackend(MongoEngineBackend):
    """
    Twitter authentication.
    """

    def authenticate(self, twitter_token=None, request=None):
        twitter_auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        twitter_auth.set_access_token(twitter_token.key, twitter_token.secret)
        api = tweepy.API(twitter_auth)
        twitter_user = api.me()
        user, created = self.user_class.objects.get_or_create(
            twitter_id = twitter_user.id,
            defaults = {
                'username': twitter_user.screen_name,
                'first_name': twitter_user.name,
            }
        )
        user.twitter_token_key = twitter_token.key
        user.twitter_token_secret = twitter_token.secret
        user.save()
        return user
