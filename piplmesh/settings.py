# -*- coding: utf-8 -*-
#
# Development Django settings for PiplMesh project.

import datetime, os

MONGO_DATABASE_NAME = 'PiplMesh'

import mongoengine
mongoengine.connect(MONGO_DATABASE_NAME, tz_aware=True)

settings_dir = os.path.abspath(os.path.dirname(__file__))

import djcelery
djcelery.setup_loader()

from celery.task.schedules import crontab

# Dummy function, so that "makemessages" can find strings which should be translated.
_ = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# A tuple that lists people who get code error notifications. When
# DEBUG=False and a view raises an exception, Django will e-mail these
# people with the full exception information. Each member of the tuple
# should be a tuple of (Full name, e-mail address).
ADMINS = ()

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Ljubljana'
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'sl'

LANGUAGES = (
    ('sl', _('Slovenian')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(settings_dir, 'locale'),
)

URL_VALIDATOR_USER_AGENT = 'Django'

SITE_NAME = 'PiplMesh'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = os.path.join(settings_dir, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(settings_dir, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'piplmesh.panels.staticfiles.finders.PanelsDirectoriesFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Used to reconstruct absolute/full URLs where request is not available
DEFAULT_REQUEST = {
    'SERVER_NAME': '127.0.0.1',
    'SERVER_PORT': '8000',
}

DEFAULT_FILE_STORAGE = 'piplmesh.utils.storage.GridFSStorage'

# URL prefix for internationalization URLs
I18N_URL = '/i18n/'

# List of configured IPs from which django-pushserver passthrough callbacks are allowed
INTERNAL_IPS = (
    '127.0.0.1',
)

# URL prefix for django-pushserver passthrough callbacks
PUSH_SERVER_URL = '/passthrough/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '02dl2nfiacp)87-1g2$=l@b(q5+qs^)qo=byzdvgx+35q)gw&^'

EMAIL_HOST = 'localhost'
EMAIL_SUBJECT_PREFIX = '[PiplMesh] '
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'piplmesh.panels.loaders.panels_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    'django_browserid.context_processors.browserid_form',
    'piplmesh.frontend.context_processors.global_vars',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'piplmesh.account.middleware.LazyUserMiddleware',
    'piplmesh.account.middleware.UserBasedLocaleMiddleware',
    'piplmesh.frontend.middleware.NodesMiddleware',
)

ROOT_URLCONF = 'piplmesh.urls'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#   os.path.join(settings_dir, 'templates'),
)

INSTALLED_APPS = (
    # Ours are first so that we can override default templates in other apps
    'piplmesh.account',
    'piplmesh.api',
    'piplmesh.frontend',
    'piplmesh.nodes',
    'piplmesh.utils',
    'piplmesh.panels',
    'piplmesh.panels.horoscope', # To load manage.py command

    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'pushserver',
    'djcelery',
    'tastypie',
    'tastypie_mongoengine',
    'sekizai',
    'missing',
    'django_browserid',
)

PUSH_SERVER = {
    'port': 8001,
    'address': '127.0.0.1',
    'store': {
        'type': 'memory',
        'min_messages': 0,
        'max_messages': 100,
        'message_timeout': 10,
    },
    'locations': (
        {
            'type': 'subscriber',
            'url': r'/updates/(.+)/',
            'polling': 'long',
            'create_on_get': True,
            'allow_origin': 'http://127.0.0.1:8000',
            'allow_credentials': True,
            'passthrough': 'http://127.0.0.1:8000' + PUSH_SERVER_URL,
        },
        {
            'type': 'publisher',
            'url': r'/send-update/(.+)/',
        },
    ),
}

CHECK_ONLINE_USERS_INTERVAL = 10 # seconds
CHECK_FOR_NEW_HOROSCOPE = 6 # am every day
POLL_BICIKELJ_INTERVAL = 60 # seconds

CELERY_RESULT_BACKEND = 'mongodb'
CELERY_MONGODB_BACKEND_SETTINGS = {
    'host': '127.0.0.1',
    'port': 27017,
    'database': 'celery',
    'taskmeta_collection': 'celery_taskmeta',
}

BROKER_URL = 'mongodb://127.0.0.1:27017/celery'

CELERY_ENABLE_UTC = USE_TZ
CELERY_TIMEZONE = TIME_ZONE

CELERYBEAT_SCHEDULE = {
    'check_online_users': {
        'task': 'piplmesh.frontend.tasks.check_online_users',
        'schedule': datetime.timedelta(seconds=CHECK_ONLINE_USERS_INTERVAL),
        'args': (),
    },
    'update_horoscope': {
        'task': 'piplmesh.panels.horoscope.tasks.update_horoscope',
        'schedule': crontab(hour=CHECK_FOR_NEW_HOROSCOPE),
        'args': (),
    },
    'update_station_info': {
        'task': 'piplmesh.panels.bicikelj.tasks.update_station_info',
        'schedule': datetime.timedelta(seconds=POLL_BICIKELJ_INTERVAL),
        'args': (),
    },
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_REDIRECT_URL = '/'

SESSION_ENGINE = 'mongoengine.django.sessions'

AUTHENTICATION_BACKENDS = (
    'piplmesh.account.backends.MongoEngineBackend',
    'piplmesh.account.backends.FacebookBackend',
    'piplmesh.account.backends.TwitterBackend',
    'piplmesh.account.backends.FoursquareBackend',
    'piplmesh.account.backends.GoogleBackend',
    'piplmesh.account.backends.BrowserIDBackend',
    'piplmesh.account.backends.LazyUserBackend',
)

TEST_RUNNER = 'tastypie_mongoengine.test_runner.MongoEngineTestSuiteRunner'
TEST_RUNNER_FILTER = (
    'piplmesh.',
)

NODES_BACKENDS = (
    'piplmesh.nodes.backends.RandomNodesBackend',
)

NODES_MIDDLEWARE_EXCEPTIONS = (
    MEDIA_URL,
    STATIC_URL,
    I18N_URL,
    PUSH_SERVER_URL,
)

# Facebook settings
# Site URL for Facebook app is set to http://127.0.0.1:8000/
# so run your development server on port 8000
# and access your site by local ip 127.0.0.1:8000 in your browser
FACEBOOK_APP_ID = '268978083181801' # Add your app ID/API key
FACEBOOK_APP_SECRET = '0d86323405308915be0564e8c00bf6e0' # Add your app secret key
FACEBOOK_LOGIN_REDIRECT = '/' # Redirects here after login
FACEBOOK_ERROR_REDIRECT = '/' # Redirects here if user is not connected with Facebook

# Twitter settings
TWITTER_CONSUMER_KEY = 'yeZOtec5ol5I9BGCCKpcw'
TWITTER_CONSUMER_SECRET = 'Dv80Q51jx8FWDInmZCGZs8AKDnRwAdrS0lxgZA4NWs'
TWITTER_LOGIN_REDIRECT = '/'

# Foursquare settings
FOURSQUARE_CLIENT_ID = 'IU4LBMWT2DOCQ2JOIN3A04450HBB4GY2D5QX0WYPQ2DLP1DK'
FOURSQUARE_CLIENT_SECRET = 'UDFGDOKUSOOV0GGGI0JDHR5OOJ1KBVV3OJ50SOGFVFJ3YPKO'
FOURSQUARE_LOGIN_REDIRECT = '/'

# Google settings
GOOGLE_CLIENT_ID = '961599639127.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'XjLBcVysDl6g0qEx_bnGUPDb'
GOOGLE_LOGIN_REDIRECT = '/'

# You can set up your own custom search engine on: http://www.google.com/cse/
# just register with you google account and crate new search engine.
# When you create new search engine, switch uniqe id with your own and new settings will apply.
# If want to change some settings that needs to be changed in the source code to take effect,
# you will be explicitly warned that you have to change the code to take effect, before you will make the change.
# Current settings are autocomplete, searching whole web.
SEARCH_ENGINE_UNIQUE_ID = '003912915932446183218:zeq20qye9oa'

DEFAULT_USER_IMAGE = 'piplmesh/images/unknown.png'

CSRF_FAILURE_VIEW = 'piplmesh.frontend.views.forbidden_view'

# We are using rfc-2822 because it's better supported when parsing dates in JavaScript
TASTYPIE_DATETIME_FORMATTING = 'rfc-2822'
