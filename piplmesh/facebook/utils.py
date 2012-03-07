import json
import urllib

from core.models import Profile

def fb(self, user=None, page=None, token=None):
    """ 
    Format Facebook Graph API URL. 
    """
    
    param = ''
    if user:
        profile = Profile.objects.get(user=user)
    if user and token:
        param = '?access_token=%s' % profile.token
    results = 'https://graph.facebook.com/%s/%s' % (self, param)
    return results

def valid_token(self):
    """ 
    Check to see if a user's Facebook token is still valid. 
    """
    
    if self.is_authenticated():
        url = urllib.urlopen('%s' % fb('me', self, token=True))
        data = json.load(url)
    if not 'error' in data:
        results = True
        
    return results
