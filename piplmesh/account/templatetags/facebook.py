import json, urllib

from django import template
from django.contrib.auth import models

from piplmesh.account import models, utils

register = template.Library()

@register.simple_tag
def facebook_graph(self):
    """ 
    Facebook graph for a specific user. 
    """
    
    data = urllib.urlopen('%s' % utils.graph_api_url('me', self, token=True))
    results = json.load(data)
    return results

@register.filter
def valid_token(user):
    """ 
    Check if user's Facebook token is still valid.
    """
  
    results = None
    if user.is_authenticated():
        if utils.token(user):
            results = True

    return results
