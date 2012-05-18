from django import template
from django.conf import settings

import tweepy

register = template.Library()

@register.simple_tag
def twitter_picture(key, secret):
    twitter_auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    twitter_auth.set_access_token(key, secret)
    return tweepy.API(twitter_auth).me().profile_image_url
