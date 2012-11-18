import math

from django.core import exceptions
from django.utils import importlib

LATITUDE_SESSION_KEY = '_latitude'
LONGITUDE_SESSION_KEY = '_longitude'

SESSION_KEY = '_nodes_id'
BACKEND_SESSION_KEY = '_nodes_backend'
CLOSEST_LATITUDE_SESSION_KEY = '_nodes_latitude'
CLOSEST_LONGITUDE_SESSION_KEY = '_nodes_longitude'
MOCKING_SESSION_KEY = '_nodes_mocking'

def is_mocking(request):
    return request.session.get(MOCKING_SESSION_KEY, False)

def flush_session(request):
    for key in (SESSION_KEY, BACKEND_SESSION_KEY, CLOSEST_LATITUDE_SESSION_KEY, CLOSEST_LONGITUDE_SESSION_KEY, MOCKING_SESSION_KEY):
        try:
            del(request.session[key])
        except KeyError:
            pass

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

def get_node(request, allow_mocking=True):
    """
    Returns wireless node from which request originated. Or the closest
    wireless node based on geolocation data stored in request session.

    Returns ``None`` if no node could be determined.
    """

    # TODO: What if user moves from inside to outside, or outside to inside, inside existing session? How should we invalidate node?
    # TODO: What if user moves between nodes, between outside locations?

    node = None
    try:
        node_id = request.session[SESSION_KEY]
        backend_path = request.session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        node = backend.get_node(node_id)
        mocking = is_mocking(request)

        # Return node if mocking is in progress and user is authenticated
        if allow_mocking and mocking and request.user and request.user.is_authenticated() and request.user.is_staff:
            return node
        # If mocking was in progress and user isn't allowed to mock reset nodes value
        elif mocking:
            node = None
            mocking = False

    except KeyError:
        pass

    if node is not None:
        node._outside_request = CLOSEST_LATITUDE_SESSION_KEY in request.session or CLOSEST_LONGITUDE_SESSION_KEY in request.session
        if node.is_inside_request():
            if LATITUDE_SESSION_KEY not in request.session and LONGITUDE_SESSION_KEY not in request.session:
                return node
        elif node.is_outside_request():
            if request.session.get(CLOSEST_LATITUDE_SESSION_KEY) == request.session.get(LATITUDE_SESSION_KEY) and request.session.get(CLOSEST_LONGITUDE_SESSION_KEY) == request.session.get(LONGITUDE_SESSION_KEY):
                return node

    node = None
    flush_session(request)

    for backend in get_backends():
        node = backend.get_source_node(request)
        if node is None:
            continue

        request.session[SESSION_KEY] = node.id
        request.session[BACKEND_SESSION_KEY] = backend.get_full_name()

        return node

    if LATITUDE_SESSION_KEY not in request.session or LONGITUDE_SESSION_KEY not in request.session:
        return None

    assert node is None

    node_backend = None
    for backend in get_backends():
        new_node = backend.get_closest_node(request, request.session[LATITUDE_SESSION_KEY], request.session[LONGITUDE_SESSION_KEY])
        if new_node is None:
            continue

        # Compare our current best match with the new one
        if node is None or distance(request.session[LATITUDE_SESSION_KEY], request.session[LONGITUDE_SESSION_KEY], new_node.latitude, new_node.longitude) < distance(request.session[LATITUDE_SESSION_KEY], request.session[LONGITUDE_SESSION_KEY], node.latitude, node.longitude):
            node_backend = backend.get_full_name()
            node = new_node

    if node is None:
        return None

    node._outside_request = True

    request.session[SESSION_KEY] = node.id
    request.session[BACKEND_SESSION_KEY] = node_backend
    request.session[CLOSEST_LATITUDE_SESSION_KEY] = request.session[LATITUDE_SESSION_KEY]
    request.session[CLOSEST_LONGITUDE_SESSION_KEY] = request.session[LONGITUDE_SESSION_KEY]

    return node

def get_all_nodes():
    """
    Returns an iterator over all known nodes.
    """

    for backend in get_backends():
        for node in backend.get_all_nodes():
            yield node
