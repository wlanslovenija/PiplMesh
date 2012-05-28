import json, urllib

def graph_api_url(fb_user_id, user=None, page=None, token=None):
    """ 
    Format Facebook Graph API URL. 
    """
    
    param = ''
    if user and token:
        param = '?access_token=%s' % user.facebook_token
    results = 'https://graph.facebook.com/%s/%s' % (fb_user_id, param)
    return results

def valid_token(user):
    """ 
    Check to see if a user's Facebook token is still valid. 
    """
    
    if user.is_authenticated():
        url = urllib.urlopen('%s' % graph_api_url('me', user, token=True))
        data = json.load(url)
    if not 'error' in data:
        results = True
        
    return results