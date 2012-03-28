import json, urllib

from piplmesh.account import models

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

def initial_accepts_request(request, form_class):
    """
    If fields in the given form uses dynamic initial values which accepts request argument
    it wraps them so that request is given to them when called.
    """

    initial = {}
 
    for name, field in form_class.base_fields.items():
        if callable(field.initial):
            try:
                if len(inspect.getargspec(field.initial)[0]) == 1:
                    # We fight Python aliasing in for loops here
                    initial[name] = (lambda fi: lambda: fi(request))(field.initial)
            except:
                pass
	 
    if not initial:
        return form_class
	 
    def wrapper(*args, **kwargs):
        initial.update(kwargs.get('initial', {}))
        kwargs['initial'] = initial
        return form_class(*args, **kwargs)
	 
    return wrapper