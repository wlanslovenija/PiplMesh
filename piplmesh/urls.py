from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from tastypie import api

from piplmesh.account import models, views as account_views
from piplmesh.api import resources
from piplmesh.frontend import debug as debug_views, views as frontend_views

v1_api = api.Api(api_name='v1')
v1_api.register(resources.UserResource())
v1_api.register(resources.UploadedFileResource())
v1_api.register(resources.PostResource())

js_info_dict = {
    'packages': (
        'django.conf',
        'piplmesh.frontend',
    ),
}

I18N_URL = settings.I18N_URL.lstrip('/')
PUSH_SERVER_URL = settings.PUSH_SERVER_URL.lstrip('/')

urlpatterns = patterns('',
    url(r'^$', frontend_views.HomeView.as_view(), name='home'),

    url(r'^outside/$', frontend_views.OutsideView.as_view(), name='outside'),
    url(r'^search/', frontend_views.SearchView.as_view(), name='search'),

    url(r'^upload/$', frontend_views.upload_view, name='upload'),

    # Registration, login, logout
    url(r'^register/$', account_views.RegistrationView.as_view(), name='registration'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}, name='login'),
    url(r'^logout/$', account_views.logout, name='logout'),

    # Facebook
    url(r'^facebook/login/$', account_views.FacebookLoginView.as_view(), name='facebook_login'),
    url(r'^facebook/callback/$', account_views.FacebookCallbackView.as_view(), name='facebook_callback'),

    # Twitter
    url(r'^twitter/login/$', account_views.TwitterLoginView.as_view(), name='twitter_login'),
    url(r'^twitter/callback/$', account_views.TwitterCallbackView.as_view(), name='twitter_callback'),

    # Profile, account
    url(r'^user/(?P<username>' + models.USERNAME_REGEX + ')/$', frontend_views.UserView.as_view(), name='user'),
    url(r'^account/$', account_views.AccountChangeView.as_view(), name='account'),
    url(r'^account/password/change/$', account_views.PasswordChangeView.as_view(), name='password_change'),

    # RESTful API
    url(r'^api/', include(v1_api.urls)),

    # Internationalization support
    url(r'^' + I18N_URL, include('django.conf.urls.i18n')),
    url(r'^' + I18N_URL + 'js/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # Internals
    # TODO: Limit only to internal IPs
    url(r'^' + PUSH_SERVER_URL, include('pushserver.urls')),
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
