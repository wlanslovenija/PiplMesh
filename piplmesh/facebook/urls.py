from django.conf.urls.defaults import patterns, url

from facebook.views import (facebook_login, facebook_logout,
                            facebook_callback)

urlpatterns = patterns('',
    (r'^login/$', facebook_login, name='facebook_login'),
    (r'^logout/$', facebook_logout),
    url(r'^callback/$', facebook_callback, name='facebook_callback'),
)
