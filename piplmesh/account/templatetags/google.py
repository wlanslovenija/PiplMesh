import json, urllib

from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def google_picture(google_token):
    data = urllib.urlopen("https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s" % google_token)
    google_user = json.load(data)
    return google_user['picture']