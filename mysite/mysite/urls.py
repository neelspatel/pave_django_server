from django.conf.urls import patterns, include, url
from data import views as dataviews

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    url(r'^data/', include('data.urls')),
    url(r'^create/', dataviews.create, name = 'create'),
    url(r'^new/', dataviews.new, name = 'new'),    
    url(r'^admin/', include(admin.site.urls)),
)
