import json, urllib

from account import models

def graph_api_url(self, user=None, page=None, token=None):
    """ 
    Format Facebook Graph API URL. 
    """
    
    param = ''
    if user:
        profile = models.UserProfile.objects.get(user=user)
    if user and token:
        param = '?access_token=%s' % profile.token
    results = 'https://graph.facebook.com/%s/%s' % (self, param)
    return results

def valid_token(self):
    """ 
    Check to see if a user's Facebook token is still valid. 
    """
    
    if self.is_authenticated():
        url = urllib.urlopen('%s' % graph_api_url('me', self, token=True))
        data = json.load(url)
    if not 'error' in data:
        results = True
        
    return results
