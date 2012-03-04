import urllib, hashlib

from django import template
from django.conf import settings
from django.contrib.sites import models as sites_models

register = template.Library()

@register.inclusion_tag('gravatar.html')
def gravatar(email, size=50, default='unknown.png'):
    """
    Gravatar function return avatar image depends on user email.

    Sample usage::
        {% load gravatar %}
        {% gravatar "piplmesh@piplmesh" 50 %}
    """

    schema = 'https' if getattr(settings, 'GRAVATAR_HTTPS_DEFAULT', False) else 'http'

    domain = sites_models.Site.objects.get_current().domain

    # Construct the url for default avatar and gravatar services
    default_avatar_url = "%(schema)s://%(domain)s%(static_url)spiplmesh/images/%(avatar)s" % {
        "schema": schema,
        "domain": domain,
        "static_url": settings.STATIC_URL,
        "avatar": default
    }

    gravatar_url = "https://secure.gravatar.com/avatar/%(email_hash)s?s=%(size)s&d=%(default_avatar)s" % {
        "email_hash": hashlib.md5(email.lower()).hexdigest(),
        "size": size,
        "default_avatar": urllib.quote(default_avatar_url)
    }

    return {
        'gravatar': {
            'url': gravatar_url,
            'size': size
        }
    }