from django.conf.urls import patterns, url
from data import views

urlpatterns = patterns('',
	url(r'detail', views.detail, name='detail'),    
	url(r'randomquestion', views.randomQuestion, name = 'random'),
	url(r'newuser', views.newUser, name = 'newuser'),
	url(r'newanswer', views.newAnswer, name = 'newanswer'),
	url(r'^getfeedobject/(?P<feed_object_id>\w+)/$', views.getFeedObject, name='getfeedobject'),
	url(r'^getuser/(?P<user_id>\w+)/$', views.getUser, name='getuser'),
	url(r'^getallfeedobjects/(?P<user_id>\w+)/$', views.getAllFeedObjects, name='getallfeedbackobjects'),
	url(r'^getinsight/(?P<user_id>\w+)/$', views.getInsight, name = "getinsight"),
	url(r'^getlistquestions/(?P<user_id>\w+)/$', views.getListQuestionsNew, name = "getlistquestions"),	
	url(r'^getlistquestionsnew/(?P<user_id>\w+)/$', views.getListQuestionsNew, name = "getlistquestionsnew"),
	url(r'^getallanswers/(?P<user_id>\w+)/$', views.getAllAnswers, name = "getallanswers"),
	url(r'^gettrendingobjects/(?P<number>\w+)/$', views.getTrendingObjects, name = "gettrendingobjects",)

)
