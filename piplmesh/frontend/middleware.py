from django import http
from django.conf import settings
from django.core import urlresolvers

from piplmesh import nodes

class NodesMiddleware(object):
    def process_request(self, request):
        outside_url = urlresolvers.reverse('outside')
        request.node = nodes.get_node(request)

        if request.path == outside_url:
            if request.node is None:
                # We do nothing special for outside view if request
                # is from outside and without geolocation data
                return None
            elif settings.DEBUG:
                # We allow access if request is from inside if DEBUG is true
                # (So that we can test the view)
                request.node = None
                return None
            else:
                # Otherwise we redirect to home
                return http.HttpResponseRedirect(urlresolvers.reverse('home'))

        for exception in getattr(settings, 'NODES_MIDDLEWARE_EXCEPTIONS', ()):
            if request.path.startswith(exception):
                return None

        if request.node is None:
            # Outside request and without geolocation data, we redirect
            return http.HttpResponseRedirect(outside_url)
        else:
            # Inside request, or request with geolocation data, we do not do anything
            return None
