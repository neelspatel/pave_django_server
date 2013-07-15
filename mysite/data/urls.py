from django.conf.urls import patterns, url
from data import views, ugviews, notif_views, group_views, training_views

urlpatterns = patterns('',
	
        url(r'uploadImage', views.uploadImage, name = "uploadProductImage"),
        url(r'^imagesearch/(?P<query>\w+)/$', views.imagesearch, name = "imagesearch"),
	url(r'uploadugproduct', ugviews.uploadUGProductImage, name = "uploadProductImage"),
        url(r'^gettrainingquestions/(?P<user_id>\w+)/$', views.getListQuestionsForPersonalityType, name = "getlistquestionsnew"),
	url(r'transferanswers', views.transferAnswers, name='transferAnswers'),
        url(r'^updatetopfriends/(?P<user_id>\w+)/$', views.updateTopFriends, name = "createUGQuestion"),
        url(r'^createugquestion/(?P<user_id>\w+)/$', ugviews.createUGQuestion, name = "createUGQuestion"),
	url(r'checkimage', views.checkimage, name= 'checkimage'),
        url(r'rebase', views.rebase, name= 'rebase'),
	url(r'detail', views.detail, name='detail'),    
	url(r'randomquestion', views.randomQuestion, name = 'random'),
	url(r'newuser', views.newUser, name = 'newuser'),
	url(r'newanswer', views.newAnswer, name = 'newanswer'),
	url(r'batchcreateproducts', views.batchCreateProducts, name = 'batchcreateproducts'),
	url(r'batchcreateanswers', views.batchCreateAnswers, name = 'batchcreateanswers'),
	url(r'batchcreatequestions', views.batchCreateQuestions, name = 'batchcreatequestions'),
	url(r'^getfeedobject/(?P<feed_object_id>\w+)/$', views.getFeedObject, name='getfeedobject'),
	url(r'^getuser/(?P<user_id>\w+)/$', views.getUser, name='getuser'),
	url(r'^getallfeedobjects/(?P<user_id>\w+)/$', views.getAllFeedObjects, name='getallfeedbackobjects'),
	url(r'^getinsight/(?P<user_id>\w+)/$', views.getInsight, name = "getinsight"),
	url(r'^getlistquestions/(?P<user_id>\w+)/$', views.getListQuestionsNew, name = "getlistquestions"),	

	# endpoints for getting questions
	url(r'^getlistquestionsnew/(?P<user_id>\w+)/$', views.getListQuestionsNew, name = "getlistquestionsnew"),
	url(r'^newgetlistquestions/(?P<user_id>\w+)/$', views.newGetListQuestions, name = "newgetlistquestions"),	
	url(r'^groupgetlistquestions/(?P<user_id>\w+)/$', group_views.getGroupListQuestions, name = "getgrouplistquestions"),
	url(r'^traininggetlistquestions/(?P<user_id>\w+)/$', training_views.getTrainingListQuestions, name = "getlistquestiontraining"),
	
	# get questions to train the stupid shit
	url(r'^recsgetlistquestions/(?P<user_id>\w+)/$', training_views.getRecsListQuestions, name = "getlistquestionrecs"),
	
	url(r'^getallanswers/(?P<user_id>\w+)/$', views.getAllAnswers, name = "getallanswers"),
	url(r'^gettrendingobjects/(?P<user_id>\w+)/$', views.getTrendingObjects, name = "gettrendingobjects",),
	url(r'^numberofnewobjects/(?P<user_id>\w+)/(?P<time_since>\w+)/$', views.numberOfNewObjects, name = "number of new objects",),
        url(r'^numberofanswersgiven/(?P<user_id>\w+)/$', views.numberOfAnswersGiven, name = "number of answers given"),
	url(r'^numberofanswersgivenforjs/(?P<user_id>\w+)/$', views.numberOfAnswersGivenForJS, name = "number of answers given for js"),
)
