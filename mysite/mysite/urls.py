from django.conf.urls import patterns, include, url
from data import views as dataviews
from recs import views as recsviews

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    url(r'^data/', include('data.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'/recs', include('recs.urls'))
)
