import json, urlparse, urllib

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError

from account.models import UserProfile

class FacebookBackend:
    def authenticate(self, token=None, request=None):
        """
        Facebook authentication.

        Retrieve access token and Facebook data. Determine if user already has a
        profile. If not, a new profile is created using either the user's
        username or Facebook id. Finally, the user's Facebook data is saved.
        """
    
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': request.build_absolute_uri(reverse('facebook_callback')),
            'code': token,
        }
    
        # Retrieve access token
        url = urllib.urlopen('https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode(args)).read()
        response = urlparse.parse_qs(url)
        access_token = response['access_token'][-1]
    
        # Retrieve user's public profile information
        data = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % access_token)
        fb = json.load(data)

        try:
            # Check if user profile exists
            profile = UserProfile.objects.get(fid=fb['id'])
            user = profile.user

            # Update access token
            profile.token = access_token
            profile.save()

        except UserProfile.DoesNotExist:
            # User profile doesn't exist, create new user
            username = fb.get('username', fb['id'])
            user = User.objects.create_user(username=username, email=fb['email'])
            user.first_name = fb['first_name']
            user.last_name = fb['last_name']
            user.save()

        # Create and save account user
        profile = UserProfile.objects.create(user=user, token=access_token, fid=fb['id'], gender=fb['gender'])
        profile.save()

        return user

    def get_user(self, user_id):
        """ 
        Returns user of a given ID. 
        """
    
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        supports_object_permissions = False
        supports_anonymous_user = True