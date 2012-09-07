import json, urllib

from django.conf import settings
from django.utils import crypto, translation

from mongoengine import queryset
from mongoengine.django import auth

from django_browserid import auth as browserid_auth, base as browserid_base

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

    # TODO: List all profile data fields we (can) get

    def authenticate(self, facebook_access_token, request):
        # Retrieve user's profile information
        # TODO: Handle error, what if request was denied?
        facebook_profile_data = json.load(urllib.urlopen('https://graph.facebook.com/me?%s' % urllib.urlencode({'access_token': facebook_access_token})))

        try:
            user = self.user_class.objects.get(facebook_profile_data__id=facebook_profile_data.get('id'))
        except self.user_class.DoesNotExist:
            # TODO: Based on user preference, we might create a new user here, not just link with existing, if existing user is lazy user
            # We reload to make sure user object is recent
            request.user.reload()
            user = request.user
            # TODO: Is it OK to override Facebook link if it already exist with some other Facebook user?

        user.facebook_access_token = facebook_access_token
        user.facebook_profile_data = facebook_profile_data

        if user.lazyuser_username and facebook_profile_data.get('username'):
            # TODO: Does Facebook have same restrictions on username content as we do?
            user.username = facebook_profile_data.get('username')
            user.lazyuser_username = False
        if user.first_name is None:
            user.first_name = facebook_profile_data.get('first_name') or None
        if user.last_name is None:
            user.last_name = facebook_profile_data.get('last_name') or None
        if user.email is None:
            # TODO: Do we know if all e-mail addresses given by Facebook are verified?
            # TODO: Does not Facebook support multiple e-mail addresses? Which one is given here?
            user.email = facebook_profile_data.get('email') or None
        if user.gender is None:
            # TODO: Does it really map so cleanly?
            user.gender = facebook_profile_data.get('gender') or None

        user.save()

        return user

class TwitterBackend(MongoEngineBackend):
    """
    Twitter authentication.

    Twitter profile data fields are:
        name: user's full name
        screen_name: user's username
        profile_image_url
        profile_background_image_url
        id: id of Twitter user
        id_str: string id of Twitter user
        created_at: full date of user's registration on Twitter
        location: user's location
        time_zone
        lang: user's preferred language
        url: URL of user's website
        description: user's description of themselves
        profile_sidebar_fill_color
        profile_text_color
        profile_background_color
        profile_link_color
        profile_sidebar_border_color
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
        verified: boolean value; tells whether user's email is verified
        protected: boolean value
        show_all_inline_media: boolean value
        is_translator: boolean value
        profile_background_tile: boolean value
        contributors_enabled: boolean value
        utc_offset: integer
    """

    def authenticate(self, twitter_access_token, request):
        twitter_auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        twitter_auth.set_access_token(twitter_access_token.key, twitter_access_token.secret)
        twitter_api = tweepy.API(twitter_auth)

        twitter_profile_data = twitter_api.me()

        try:
            user = self.user_class.objects.get(twitter_profile_data__id=twitter_profile_data.get('id'))
        except self.user_class.DoesNotExist:
            # TODO: Based on user preference, we might create a new user here, not just link with existing, if existing user is lazy user
            # We reload to make sure user object is recent
            request.user.reload()
            user = request.user
            # TODO: Is it OK to override Twitter link if it already exist with some other Twitter user?

        user.twitter_access_token = models.TwitterAccessToken(key=twitter_access_token.key, secret=twitter_access_token.secret)
        user.twitter_profile_data = twitter_profile_data

        if user.lazyuser_username and twitter_profile_data.get('screen_name'):
            # TODO: Does Twitter have same restrictions on username content as we do?
            user.username = twitter_profile_data.get('screen_name')
            user.lazyuser_username = False
        if user.first_name is None:
            user.first_name = twitter_profile_data.get('name') or None

        user.save()

        return user

class GoogleBackend(MongoEngineBackend):
    """
    Google authentication.

    Google profile data fields are:
        family_name: last name
        given_name: first name
        name: full name
        link: URL of Google user profile page
        picture: URL of profile picture
        locale: the language Google user is using
        gender: the gender of Google user (other|female|male)
        timezone: the default timezone of Google user
        email: Google email of user
        id: id of Google user; should be a string
        verified_email: True, if email is verified by Google API
    """

    def authenticate(self, google_access_token, request):
        # Retrieve user's profile information
        # TODO: Handle error, what if request was denied?
        google_profile_data = json.load(urllib.urlopen('https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s' % google_access_token))

        try:
            user = self.user_class.objects.get(google_profile_data__id=google_profile_data.get('id'))
        except self.user_class.DoesNotExist:
            # TODO: Based on user preference, we might create a new user here, not just link with existing, if existing user is lazy user
            # We reload to make sure user object is recent
            request.user.reload()
            user = request.user
            # TODO: Is it OK to override Google link if it already exist with some other Google user?

        user.google_access_token = google_access_token
        user.google_profile_data = google_profile_data
        
        username_guess = google_profile_data.get('email', '').rsplit('@', 1)[0]

        if user.lazyuser_username and username_guess:
            # Best username guess we can get from Google OAuth
            user.username = username_guess
            user.lazyuser_username = False
        if user.first_name is None:
            user.first_name = google_profile_data.get('given_name') or None
        if user.last_name is None:
            user.last_name = google_profile_data.get('family_name') or None
        if user.email is None:
            user.email = google_profile_data.get('email') or None
            if google_profile_data.get('verified_email'):
                user.email_confirmed = True
        if user.gender is None:
            # TODO: Does it really map so cleanly?
            user.gender = google_profile_data.get('gender') or None

        user.save()

        return user

class FoursquareBackend(MongoEngineBackend):
    """
    Foursquare authentication.

    Foursquare profile data fields are:
        id: a unique identifier for this user.
        firstName: user's first name
        lastName: user's last name
        homeCity: user's home city
        photo: URL of a profile picture for this user
        gender: user's gender: male, female, or none
        relationship: the relationship of the acting user (me) to this user (them) (optional)
        type: one of page, celebrity, or user
        contact: an object containing none, some, or all of twitter, facebook, email, and phone
        pings: pings from this user (optional)
        badges: contains the count of badges for this user, may eventually contain some selected badges
        checkins: contains the count of checkins by this user, may contain the most recent checkin as an array
        mayorships: contains the count of mayorships for this user and an items array that for now is empty
        tips: contains the count of tips from this user, may contain an array of selected tips as items
        todos: contains the count of todos this user has, may contain an array of selected todos as items
        photos: contains the count of photos this user has, may contain an array of selected photos as items
        friends: contains count of friends for this user and groups of users who are friends
        followers: contains count of followers for this user, if they are a page or celebrity
        requests: contains count of pending friend requests for this user
        pageInfo: contains a detailed page, if they are a page
    """

    def authenticate(self, foursquare_access_token, request):
        # Retrieve user's profile information
        # TODO: Handle error, what if request was denied?
        foursquare_profile_data = json.load(urllib.urlopen('https://api.foursquare.com/v2/users/self?%s' % urllib.urlencode({'oauth_token': foursquare_access_token})))['response']['user']

        try:
            user = self.user_class.objects.get(foursquare_profile_data__id=foursquare_profile_data.get('id'))
        except self.user_class.DoesNotExist:
            # TODO: Based on user preference, we might create a new user here, not just link with existing, if existing user is lazy user
            # We reload to make sure user object is recent
            request.user.reload()
            user =  request.user
            # TODO: Is it OK to override Foursquare link if it already exist with some other Foursquare user?

        user.foursquare_access_token = foursquare_access_token
        user.foursquare_profile_data = foursquare_profile_data
        
        username_guess = foursquare_profile_data.get('contact', {}).get('email', '').rsplit('@', 1)[0]

        if user.lazyuser_username and username_guess:
            # Best username guess we can get from Foursquare
            user.username = username_guess
            user.lazyuser_username = False
        if user.first_name is None:
            user.first_name = foursquare_profile_data.get('firstName') or None
        if user.last_name is None:
            user.last_name = foursquare_profile_data.get('lastName') or None
        if user.email is None:
            user.email = foursquare_profile_data.get('contact', {}).get('email') or None
        if user.gender is None:
            # TODO: Does it really map so cleanly?
            user.gender = foursquare_profile_data.get('gender') or None

        user.save()

        return user

class BrowserIDBackend(MongoEngineBackend, browserid_auth.BrowserIDBackend):
    """
    Persona authentication.

    Persona profile data fields are:
        email: email user uses for Persona
    """
    
    def authenticate(self, browserid_assertion=None, browserid_audience=None, request=None):
        result = browserid_base.verify(browserid_assertion, browserid_audience)
        if not result:
            return None

        email = result['email']

        try:
            user = self.user_class.objects.get(browserid_profile_data__email=email)
            # TODO: What is we get more than one user?
        except self.user_class.DoesNotExist:
            # TODO: Based on user preference, we might create a new user here, not just link with existing, if existing user is lazy user
            # We reload to make sure user object is recent
            request.user.reload()
            user = request.user
            # TODO: Is it OK to override BrowserID link if it already exist with some other BrowserID user?
        
        user.browserid_profile_data = result
        
        if user.lazyuser_username:
            # Best username guess we can get from BrowserID
            user.username = email.rsplit('@', 1)[0]
            user.lazyuser_username = False
        if user.email is None:
            user.email = email or None
            # BrowserID takes care of email confirmation
            user.email_confirmed = True

        user.save()

        return user

class LazyUserBackend(MongoEngineBackend):
    def authenticate(self, request):
        while True:
            try:
                username = LAZYUSER_USERNAME_TEMPLATE % crypto.get_random_string(6)
                user = self.user_class.objects.create(
                    username=username,
                    language=translation.get_language_from_request(request),
                )
                break
            except queryset.OperationError, e:
                msg = str(e)
                if 'E11000' in msg and 'duplicate key error' in msg and 'username' in msg:
                    continue
                raise

        return user
