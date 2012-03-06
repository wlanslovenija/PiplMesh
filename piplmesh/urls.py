from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from piplmesh.frontend import views as frontend_views

urlpatterns = patterns('',
    url('^$', frontend_views.HomeView.as_view(), name='home'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # registration, login, logout
    url(r'^register/$', 'account.views.registration_view', name='registration'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
    # Facebook
    url(r'^facebook/', include('facebook.urls')),
)
