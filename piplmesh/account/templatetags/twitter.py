from django import template
from django.conf import settings

import tweepy

register = template.Library()

@register.simple_tag
def twitter_picture(token_key, token_secret):
    twitter_auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    twitter_auth.set_access_token(token_key, token_secret)
    return tweepy.API(twitter_auth).me().profile_image_url
