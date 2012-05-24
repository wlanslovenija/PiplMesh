from django.conf.urls.defaults import patterns, include, url

from tastypie import api

from piplmesh.account import models, views as account_views
from piplmesh.api import resources
from piplmesh.frontend import views as frontend_views

v1_api = api.Api(api_name='v1')
v1_api.register(resources.UserResource())
v1_api.register(resources.PostResource())

urlpatterns = patterns('',
    url('^$', frontend_views.HomeView.as_view(), name='home'),

    url(r'^search/', frontend_views.SearchView.as_view(), name='search'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^passthrough/', include('pushserver.urls')),

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

    # Profile, Account
    url(r'^user/(?P<username>' + models.USERNAME_REGEX + ')/$', frontend_views.UserView.as_view(), name='user'),
    url(r'^account/$', account_views.AccountChangeView.as_view(), name='account'),
    url(r'^account/password/change/$', account_views.PasswordChangeView.as_view(), name='password_change'),

    # RESTful API
    url(r'^api/', include(v1_api.urls)),
)
