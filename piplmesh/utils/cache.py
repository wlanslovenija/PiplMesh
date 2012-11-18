import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.core.cache.backends import base
from django.utils import timezone

import bson
import mongoengine

# TODO: Implement get_many, set_many, and delete_many

class MongoEngineCache(base.BaseCache):
    def __init__(self, location, params):
        super(MongoEngineCache, self).__init__(params)

        class Cache(mongoengine.Document):
            key = mongoengine.StringField(required=True, unique=True)
            expire = mongoengine.DateTimeField(required=True)
            value = mongoengine.DynamicField(required=True)

            meta = {
                'collection': location or 'cache',
            }

        self._cache_class = Cache

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        try:
            obj = self._cache_class.objects(key=key, expire__gte=timezone.now()).get()

            if isinstance(obj.value, int):
                return obj.value
            else:
                try:
                    return pickle.loads(obj.value)
                except pickle.PickleError:
                    return default

        except self._cache_class.DoesNotExist:
            return default

    def _set(self, key, value, timeout, version, fun):
        if timeout is None:
            timeout = self.default_timeout

        key = self.make_key(key, version=version)
        self.validate_key(key)

        if isinstance(value, int):
            fun(key, value, timezone.now() + datetime.timedelta(seconds=timeout))
            return

        try:
            pickled = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
            fun(key, bson.Binary(pickled), timezone.now() + datetime.timedelta(seconds=timeout))
        except pickle.PickleError:
            pass

    def _insert(self, key, value, expire):
        self._cache_class.objects.create(key=key, value=value, expire=expire, safe=True, force_insert=True)

    def _upsert(self, key, value, expire):
        self._cache_class.objects(key=key).update(set__value=value, set__expire=expire, upsert=True, safe_update=True)

    def add(self, key, value, timeout=None, version=None):
        try:
            self._set(key, value, timeout, version, self._insert)
            return True
        except mongoengine.OperationError:
            return False

    def set(self, key, value, timeout=None, version=None):
        self._set(key, value, timeout, version, self._upsert)

    def incr(self, key, delta=1, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        if self._cache_class.objects(key=key, expire__gte=timezone.now()).update(inc__value=delta, safe_update=True) == 0:
            raise ValueError

        return self.get(key, version=version)

    def has_key(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        return self._cache_class.objects(key=key, expire__gte=timezone.now()).count() > 0

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        self._cache_class.objects(key=key).delete(safe=True)

    def clear(self):
        self._cache_class.drop_collection()
