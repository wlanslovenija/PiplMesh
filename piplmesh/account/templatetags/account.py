from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings

from piplmesh.account import models

register = template.Library()

@register.inclusion_tag('user_image.html', takes_context=True)
def user_image(context, user=None):
    if user==None:
        user = context['user']
    
    return {
        'user_image': {
            'url': user.image_url(context['request'].build_absolute_uri(staticfiles_storage.url(settings.DEFAULT_IMAGE_PATH))),
            'class': '50_50'
        }
    }