from django.conf.urls.defaults import patterns, include, url

from piplmesh.account import views as account_views
from piplmesh.frontend import views as frontend_views

urlpatterns = patterns('',
    url('^$', frontend_views.HomeView.as_view(), name='home'),

    url(r'^search', frontend_views.SearchView.as_view(), name='search'),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # Registration, login, logout
    url(r'^register/$', account_views.registration_view, name='registration'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
    # Facebook
    url(r'^facebook/login/$', account_views.facebook_login, name='facebook_login'),
    url(r'^facebook/logout/$', account_views.facebook_logout, name='facebook_logout'),
    url(r'^facebook/callback/$', account_views.facebook_callback, name='facebook_callback'),
)
