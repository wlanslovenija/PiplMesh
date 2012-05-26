import urllib, json

from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def foursquare_picture(foursquare_token):
    data = urllib.urlopen('https://api.foursquare.com/v2/users/self?oauth_token=%s' % foursquare_token)
    foursquare_data = json.load(data)
    return foursquare_data.get('response').get('user').get('photo')