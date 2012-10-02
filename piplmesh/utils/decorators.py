import functools

from django.core import cache

LOCK_EXPIRE = 60 * 5 # lock expires in 5 minutes

# Based on: http://stackoverflow.com/a/7668350/252025
def single_instance_task(timeout=LOCK_EXPIRE):
    def task_exc(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock_id = 'celery-single-instance-%s' % func.__name__
            acquire_lock = lambda: cache.cache.add(lock_id, 'true', timeout)
            release_lock = lambda: cache.cache.delete(lock_id)
            if acquire_lock():
                try:
                    return func(*args, **kwargs)
                finally:
                    release_lock()

            # TODO: Log that another task instance is already running and this one was skipped
        return wrapper
    return task_exc
