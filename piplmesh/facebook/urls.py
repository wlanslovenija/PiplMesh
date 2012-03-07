from django.conf.urls.defaults import patterns, url

from facebook.views import (facebook_login, facebook_logout, facebook_callback)

urlpatterns = patterns('',
    url(r'^login/$', facebook_login, name='facebook_login'),
    url(r'^logout/$', facebook_logout, name='facebook_logout'),
    url(r'^callback/$', facebook_callback, name='facebook_callback'),
)
