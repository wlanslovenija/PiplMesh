from django.conf.urls.defaults import patterns, include, url
from piplmesh.account import views as account_views
from piplmesh.frontend import views as frontend_views
from piplmesh.facebook import views as facebook_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^$', frontend_views.HomeView.as_view(), name='home'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # registration, login, logout
    url(r'^register/$', account_views.registration_view, name='registration'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
    # Facebook
    url(r'^facebook/login/$', facebook_views.facebook_login, name='facebook_login'),
    url(r'^facebook/logout/$', facebook_views.facebook_logout, name='facebook_logout'),
    url(r'^facebook/callback/$', facebook_views.facebook_callback, name='facebook_callback'),
)
