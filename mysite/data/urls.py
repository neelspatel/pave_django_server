from django.conf.urls import patterns, url
from data import views

urlpatterns = patterns('',
<<<<<<< HEAD
=======
        url(r'^gettrainingquestions/(?P<user_id>\w+)/$', views.getListQuestionsForPersonalityType, name = "getlistquestionsnew"),
>>>>>>> dda5277d0dc1a24ac324057027d1d9ea062059c1
	url(r'transferanswers', views.transferAnswers, name='transferAnswers'),
	url(r'checkimage', views.checkimage, name= 'checkimage'),
        url(r'rebase', views.rebase, name= 'rebase'),
	url(r'detail', views.detail, name='detail'),    
	url(r'randomquestion', views.randomQuestion, name = 'random'),
	url(r'newuser', views.newUser, name = 'newuser'),
	url(r'newanswer', views.newAnswer, name = 'newanswer'),
	url(r'batchcreateproducts', views.batchCreateProducts, name = 'batchcreateproducts'),
	url(r'batchcreateanswers', views.batchCreateAnswers, name = 'batchcreateanswers'),
	url(r'^getfeedobject/(?P<feed_object_id>\w+)/$', views.getFeedObject, name='getfeedobject'),
	url(r'^getuser/(?P<user_id>\w+)/$', views.getUser, name='getuser'),
	url(r'^getallfeedobjects/(?P<user_id>\w+)/$', views.getAllFeedObjects, name='getallfeedbackobjects'),
	url(r'^getinsight/(?P<user_id>\w+)/$', views.getInsight, name = "getinsight"),
	url(r'^getlistquestions/(?P<user_id>\w+)/$', views.getListQuestionsNew, name = "getlistquestions"),	
	url(r'^getlistquestionsnew/(?P<user_id>\w+)/$', views.getListQuestionsNew, name = "getlistquestionsnew"),
	url(r'^getallanswers/(?P<user_id>\w+)/$', views.getAllAnswers, name = "getallanswers"),
	url(r'^gettrendingobjects/(?P<user_id>\w+)/$', views.getTrendingObjects, name = "gettrendingobjects",),
	url(r'^numberofnewobjects/(?P<user_id>\w+)/(?P<time_since>\w+)/$', views.numberOfNewObjects, name = "number of new objects",),
        url(r'^numberofanswersgiven/(?P<user_id>\w+)/$', views.numberOfAnswersGiven, name = "number of answers given"),
	url(r'^numberofanswersgivenforjs/(?P<user_id>\w+)/$', views.numberOfAnswersGivenForJS, name = "number of answers given for js"),
)
