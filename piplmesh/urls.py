from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import *

from django.contrib import admin
admin.autodiscover()

from piplmesh.frontend import views as frontend_views

urlpatterns = patterns('',
    url('^$', frontend_views.HomeView.as_view(), name='home'),
    url(r'^search/$', frontend_views.SearchView.as_view(), name='/search'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
