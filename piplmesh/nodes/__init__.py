import math

from django.core import exceptions
from django.utils import importlib

SOURCE_SESSION_KEY = '_nodes_source_id'
SOURCE_BACKEND_SESSION_KEY = '_nodes_source_backend'

CLOSEST_SESSION_KEY = '_nodes_closes_id'
CLOSEST_BACKEND_SESSION_KEY = '_nodes_closest_backend'
CLOSEST_LATITUDE_SESSION_KEY = '_nodes_closest_latitude'
CLOSEST_LONGITUDE_SESSION_KEY = '_nodes_closest_longitude'

def load_backend(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = importlib.import_module(module)
    except ImportError, e:
        raise exceptions.ImproperlyConfigured('Error importing nodes backend %s: "%s"' % (path, e))
    except ValueError, e:
        raise exceptions.ImproperlyConfigured('Error importing nodes backends. Is NODES_BACKENDS a correctly defined list or tuple?')
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise exceptions.ImproperlyConfigured('Module "%s" does not define a "%s" nodes backend' % (module, attr))

    return cls()

def get_backends():
    from django.conf import settings
    backends = []
    for backend_path in getattr(settings, 'NODES_BACKENDS', ()):
        backends.append(load_backend(backend_path))
    if not backends:
        raise exceptions.ImproperlyConfigured('No nodes backends have been defined. Does NODES_BACKENDS contain anything?')
    return backends

def distance(latitude_a, longitude_a, latitude_b, longitude_b):
    latitude_a, longitude_a, latitude_b, longitude_b = map(math.radians, (latitude_a, longitude_a, latitude_b, longitude_b))
    dlongitude = longitude_b - longitude_a
    dlatitude = latitude_b - latitude_a
    a = math.sin(dlatitude / 2)**2 + math.cos(latitude_a) * math.cos(latitude_b) * math.sin(dlongitude / 2)**2
    return 2 * math.asin(math.sqrt(a))

def get_source_node(request, force=False):
    """
    Returns wireless node from which request originated.

    Returns ``None`` if request originated from somewhere
    else (VPN tunnel, Internet, mobile client, ...).
    """

    node = None
    if not force:
        try:
            node_id = request.session[SOURCE_SESSION_KEY]
            backend_path = request.session[SOURCE_BACKEND_SESSION_KEY]
            backend = load_backend(backend_path)
            node = backend.get_node(node_id)
        except KeyError:
            pass

        if node is not None:
            return node

    for backend in get_backends():
        node = backend.get_source_node(request)
        if node is None:
            continue

        # Annotate the node object with the path of the backend
        node._backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)

        break

    if node is None:
        for key in (SOURCE_SESSION_KEY, SOURCE_BACKEND_SESSION_KEY):
            try:
                del(request.session[key])
            except KeyError:
                pass

        return None

    else:
        request.session[SOURCE_SESSION_KEY] = node.id
        request.session[SOURCE_BACKEND_SESSION_KEY] = node._backend

        return node

def get_closest_node(request, latitude, longitude, force=False):
    """
    Return wireless node closest to the given position.
    """

    node = None
    if not force:
        try:
            if latitude == request.session[CLOSEST_LATITUDE_SESSION_KEY] and longitude == request.session[CLOSEST_LONGITUDE_SESSION_KEY]:
                node_id = request.session[CLOSEST_SESSION_KEY]
                backend_path = request.session[CLOSEST_BACKEND_SESSION_KEY]
                backend = load_backend(backend_path)
                node = backend.get_node(node_id)
        except KeyError:
            pass

        if node is not None:
            return node

    for backend in get_backends():
        new_node = backend.get_closest_node(request, latitude, longitude)
        if new_node is None:
            continue

        # Annotate the node object with the path of the backend
        new_node._backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)

        # Compare our current best match with the new one
        if node is None or distance(latitude, longitude, new_node.latitude, new_node.longitude) < distance(latitude, longitude, node.latitude, node.longitude):
            node = new_node

    if node is None:
        for key in (CLOSEST_LATITUDE_SESSION_KEY, CLOSEST_LONGITUDE_SESSION_KEY, CLOSEST_SESSION_KEY, CLOSEST_BACKEND_SESSION_KEY):
            try:
                del(request.session[key])
            except KeyError:
                pass

        return None

    else:
        request.session[CLOSEST_LATITUDE_SESSION_KEY] = latitude
        request.session[CLOSEST_LONGITUDE_SESSION_KEY] = longitude
        request.session[CLOSEST_SESSION_KEY] = node.id
        request.session[CLOSEST_BACKEND_SESSION_KEY] = node._backend

        return node
