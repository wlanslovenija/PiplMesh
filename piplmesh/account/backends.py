import json, urllib, urlparse

from django.conf import settings
from django.core import urlresolvers
from django.utils import crypto

from mongoengine import queryset
from mongoengine.django import auth

import tweepy

from piplmesh.account import models

LAZYUSER_USERNAME_TEMPLATE = 'guest-%s'

class MongoEngineBackend(auth.MongoEngineBackend):
    # TODO: Implement object permission support
    supports_object_permissions = False
    # TODO: Implement anonymous user backend
    supports_anonymous_user = False
    # TODO: Implement inactive user backend
    supports_inactive_user = False

    def authenticate(self, username, password):
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

    def authenticate(self, facebook_token, request):
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
        data = urllib.urlopen('https://graph.facebook.com/me?%s' % urllib.urlencode({'access_token': access_token}))
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

    Twitter user fields are:
        name: User's full name
        screen_name: User's username
        profile_image_url
        profile_background_image_url
        id: id of Twitter user
        id_str: String id of Twitter user
        created_at: Full date of user's registration on Twitter
        location: User's location
        time_zone
        lang: User's preferred language
        url: url of user's website
        description: user's description of themselves
        profile_sidebar_fill_color
        profile_text_color
        profile_background_color
        profile_link_color
        profile_sidebar_border_color
        _api: tweepy.api.api object
        friends_count
        followers_count
        statuses_count
        favourites_count
        listed_count
        notifications: boolean value
        geo_enabled: boolean value
        following: boolean value
        follow_request_sent: boolean value
        profile_use_background_image: boolean value
        verified: boolean value; checks whether user's email is verified
        protected: boolean value
        show_all_inline_media: boolean value
        is_translator: boolean value
        profile_background_tile: boolean value
        contributors_enabled: boolean value
        utc_offset: integer
    """

    def authenticate(self, twitter_token, request):
        twitter_auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        twitter_auth.set_access_token(twitter_token.key, twitter_token.secret)
        api = tweepy.API(twitter_auth)
        twitter_user = api.me()

        user, created = self.user_class.objects.get_or_create(
            twitter_id = twitter_user.id,
            defaults = {
                'username': twitter_user.screen_name,
                'first_name': twitter_user.name,
                'twitter_picture_url': twitter_user.profile_image_url,
            }
        )
        user.twitter_token_key = twitter_token.key
        user.twitter_token_secret = twitter_token.secret
        user.save()
        return user

class GoogleBackend(MongoEngineBackend):
    """
    Google authentication.

    Google user fields are:
        family_name: Last name
        given_name: First name
        name: Full name
        link: Url of Google user profile page
        picture: Url of profile picture
        locale: the language Google user is using
        gender: sex of Google user
        email: Google email of user
        id: id of Google user; should be a string
        verified_email: True, if email is verified by Google API
    """

    def authenticate(self, google_token, request):
        args = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': request.build_absolute_uri(urlresolvers.reverse('google_callback')),
            'code': google_token,
            'grant_type': 'authorization_code',
        }

        token_data = urllib.urlopen('https://accounts.google.com/o/oauth2/token', urllib.urlencode(args)).read()
        access_token = json.loads(token_data)['access_token']

        user_data = urllib.urlopen('https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s' % access_token)
        google_user = json.load(user_data)

        user, created = self.user_class.objects.get_or_create(
            google_id=google_user['id'],
            defaults = {
                'username': google_user['given_name'] + google_user['family_name'],
                'first_name': google_user['given_name'],
                'last_name': google_user['family_name'],
                'email': google_user['email'],
                'gender': google_user['gender'],
                'google_link': google_user['link'],
                'google_picture_url': google_user['picture'],
            }
        )
        user.google_token = access_token
        user.save()
        return user

class LazyUserBackend(MongoEngineBackend):
    def authenticate(self):
        while True:
            try:
                username = LAZYUSER_USERNAME_TEMPLATE % crypto.get_random_string(6)
                user = self.user_class.objects.create(
                    username=username,
                )
                break
            except queryset.OperationError, e:
                msg = str(e)
                if 'E11000' in msg and 'duplicate key error' in msg and 'username' in msg:
                    continue
                raise

        return user
