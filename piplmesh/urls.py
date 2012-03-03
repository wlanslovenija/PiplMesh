from django.conf.urls.defaults import patterns, include, url
from frontend.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^home$', MainView.as_view(template_name="home.html")),
    ('^$', MainView.as_view(template_name="home.html")),
)