import datetime, hashlib, tweepy, urllib

from django.conf import settings
from django.contrib.auth import hashers, models as auth_models
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core import mail
from django.db import models
from django.test import client
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import mongoengine
from mongoengine.django import auth

from piplmesh.account import fields, utils

LOWER_DATE_LIMIT = 366 * 120
USERNAME_REGEX = r'[\w.@+-]+'

def upper_birthdate_limit():
    return datetime.datetime.today()

def lower_birthdate_limit():
    return datetime.datetime.today() - datetime.timedelta(LOWER_DATE_LIMIT)

class Connection(mongoengine.EmbeddedDocument):
    http_if_none_match = mongoengine.StringField()
    http_if_modified_since = mongoengine.StringField()
    channel_id = mongoengine.StringField()

class User(auth.User):
    username = mongoengine.StringField(
        max_length=30,
        min_length=4,
        regex=r'^' + USERNAME_REGEX + r'$',
        required=True,
        verbose_name=_("username"),
        help_text=_("Minimal of 4 characters and maximum of 30. Letters, digits and @/./+/-/_ only."),
    )

    birthdate = fields.LimitedDateTimeField(upper_limit=upper_birthdate_limit, lower_limit=lower_birthdate_limit)
    gender = fields.GenderField()
    language = fields.LanguageField()

    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)
    facebook_link = mongoengine.StringField(max_length=100)

    twitter_id = mongoengine.IntField()
    twitter_token_key = mongoengine.StringField(max_length=150)
    twitter_token_secret = mongoengine.StringField(max_length=150)

    connections = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Connection))
    connection_last_unsubscribe = mongoengine.DateTimeField()
    is_online = mongoengine.BooleanField(default=False)

    email_validated = mongoengine.BooleanField(default=False)
    email_activation_key = mongoengine.StringField(max_length=77)

    @models.permalink
    def get_absolute_url(self):
        return ('profile', (), {'username': self.username})

    def get_profile_url(self):
        return self.get_absolute_url()

    def is_anonymous(self):
        return not self.is_authenticated()

    def is_authenticated(self):
        return self.is_active and (self.has_usable_password() or self.facebook_id is not None or self.twitter_id is not None)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
        return hashers.check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        self.password = hashers.make_password(None)
        self.save()
        return self

    def has_usable_password(self):
        return hashers.is_password_usable(self.password)

    def email_user(self, subject, message, from_email=None):
        mail.send_mail(subject, message, from_email, [self.email])

    def get_image_url(self):
        if self.twitter_id:
            twitter_auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
            twitter_auth.set_access_token(self.twitter_token_key, self.twitter_token_secret)
            return tweepy.API(twitter_auth).me().profile_image_url
        
        elif self.facebook_id:
            return '%s?type=square' % utils.graph_api_url('%s/picture' % self.username)
        
        elif self.email:
            request = client.RequestFactory(**settings.DEFAULT_REQUEST).request()
            default_url = request.build_absolute_uri(staticfiles_storage.url(settings.DEFAULT_USER_IMAGE))

            return 'https://secure.gravatar.com/avatar/%(email_hash)s?%(args)s' % {
                'email_hash': hashlib.md5(self.email.lower()).hexdigest(),
                'args': urllib.urlencode({
                    'default': default_url,
                    'size': 50,
                }),
            }

        else:
            return staticfiles_storage.url(settings.DEFAULT_USER_IMAGE)

    @classmethod
    def create_user(cls, username, email=None, password=None):
        now = timezone.now()
        if not username:
            raise ValueError("The given username must be set")
        email = auth_models.UserManager.normalize_email(email)
        user = cls(
            username=username,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            date_joined=now,
        )
        if email:
            user.email = email
        user.set_password(password)
        user.save()
        return user
