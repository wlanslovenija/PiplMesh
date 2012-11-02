from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from tastypie import api

from mongo_auth import models

from piplmesh.api import resources
from piplmesh.frontend import debug as debug_views, views as frontend_views
from piplmesh import panels

# PiplMesh panels auto-discovery
panels.panels_pool.discover_panels()

# So that we can access resources outside their request handlers
user_resource = resources.UserResource()
uploadedfile_resource = resources.UploadedFileResource()
post_resource = resources.PostResource()
notification_resource = resources.NotificationResource()

API_NAME = 'v1'
v1_api = api.Api(api_name=API_NAME)
v1_api.register(user_resource)
v1_api.register(uploadedfile_resource)
v1_api.register(post_resource)
v1_api.register(notification_resource)

js_info_dict = {
    'packages': (
        'django.conf',
    ),
}

I18N_URL = settings.I18N_URL.lstrip('/')
PUSH_SERVER_URL = settings.PUSH_SERVER_URL.lstrip('/')

urlpatterns = patterns('',
    url(r'^$', frontend_views.HomeView.as_view(), name='home'),
    
    url(r'^about/$', frontend_views.AboutView.as_view(), name='about'),
    url(r'^privacy/$', frontend_views.PrivacyView.as_view(), name='privacy'),
    url(r'^contact/$', frontend_views.ContactView.as_view(), name='contact'),   
    url(r'^outside/$', frontend_views.OutsideView.as_view(), name='outside'),
    url(r'^search/', frontend_views.SearchView.as_view(), name='search'),
    
    url(r'^upload/$', frontend_views.upload_view, name='upload'),

    # Mock location
    url(r'^location/$', frontend_views.LocationView.as_view(), name='mock_location'),

    # Authentication
    url(r'^', include('mongo_auth.contrib.urls')),
    url(r'^user/(?P<username>' + models.USERNAME_REGEX + ')/$', frontend_views.UserView.as_view(), name='profile'),

    # RESTful API
    url(r'^api/', include(v1_api.urls)),

    # Internationalization support
    url(r'^' + I18N_URL + 'js/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # Internals
    url(r'^' + PUSH_SERVER_URL, include('pushserver.urls')),

    # Panels
    url(r'^panels/collapse/$', frontend_views.panels_collapse, name='panels_collapse'),
    url(r'^panels/order/$', frontend_views.panels_order, name='panels_order'),
)

if getattr(settings, 'DEBUG', False):
    urlpatterns += patterns('',
        url(r'^uploadform/$', debug_views.UploadFormView.as_view()),
    )

handler403 = frontend_views.forbidden_view
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

if getattr(settings, 'DEBUG', False):
    urlpatterns += patterns('',
        url(r'^403/$', handler403),
        url(r'^404/$', handler404),
        url(r'^500/$', handler500),
    )

# For development, serve static and media files through Django
if getattr(settings, 'DEBUG', False):
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, 'piplmesh.utils.storage.serve')
