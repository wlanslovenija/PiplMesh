import urllib, hashlib

from django import template
from django.conf import settings
from django.contrib.sites import models as sites_models

from django.template import *
register = template.Library()

@register.inclusion_tag('gravatar.html', takes_context=True)
def gravatar(context, user, size=50, default_avatar='unknown.png'):
    """
    Gravatar template tag returns avatar image based on user's email address.

    Sample usage::

        {% load gravatar_tags %}
        {% gravatar user_object 50 %}
    """

    schema = 'https' if getattr(settings, 'GRAVATAR_HTTPS_DEFAULT', False) else 'http'

    if sites_models.Site._meta.installed:
        domain = sites_models.Site.objects.get_current().domain
    else:
        domain = sites_models.RequestSite(context['request']).domain

    # Construct the url for gravatar service with default avatar specified
    default_avatar_url = '%(schema)s://%(domain)s%(static_url)spiplmesh/images/%(default_avatar)s' % {
        'schema': schema,
        'domain': domain,
        'static_url': settings.STATIC_URL,
        'default_avatar': default_avatar,
    }

    gravatar_url = 'https://secure.gravatar.com/avatar/%(email_hash)s?s=%(size)s&d=%(default_avatar_url)s' % {
        'email_hash': hashlib.md5(user.email.lower()).hexdigest(),
        'size': size,
        'default_avatar_url': urllib.quote(default_avatar_url),
    }

    return {
        'gravatar': {
            'url': gravatar_url,
            'size': size,
        }
    }