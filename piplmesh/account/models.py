import datetime, hashlib, tweepy

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
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
    twitter_picture_url = mongoengine.StringField(max_length=150)

    google_id = mongoengine.StringField(max_length=30)
    google_token = mongoengine.StringField(max_length=150)
    google_link = mongoengine.StringField(max_length=100)
    google_picture_url = mongoengine.StringField(max_length=150)

    connections = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Connection))
    connection_last_unsubscribe = mongoengine.DateTimeField()
    is_online = mongoengine.BooleanField(default=False)
    
    def get_image_url(self, request):
        if self.twitter_id:
            return self.twitter_picture_url
        
        elif self.facebook_id:
            return '%s?type=square' % utils.graph_api_url('%s/picture' % self.username)

        elif self.google_id:
            return self.google_picture_url
        
        else:
            default_url = request.build_absolute_uri(staticfiles_storage.url(settings.DEFAULT_USER_IMAGE))

            return 'https://secure.gravatar.com/avatar/%(email_hash)s?s=50&d=%(default_url)s' % {
                'email_hash': hashlib.md5(self.email.lower()).hexdigest(),
                'default_url': default_url,
            }
