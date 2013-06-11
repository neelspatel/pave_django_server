from django.conf.urls import patterns, url

from data import views

urlpatterns = patterns('',
	url(r'^(?detail\w+)/$', views.detail, name='detail'),    
    url(r'^(?P<data_id>\w+)/$', views.detail, name='detail'),
)
