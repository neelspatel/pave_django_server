# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
from django.db.models import Q
from django.core import serializers
from data.models import Question
from data.models import User
from data.models import Notification
from data.models import Recommendation
from data.models import TrainingProductType, TrainingProduct, TrainingAnswer, TrainingQuestion 
from django.forms.models import model_to_dict
from random import randint
from random import choice
import logging
import urllib
import random
import datetime
import calendar
import requests
import itertools
import notif_views as notif_utils

PROCESSING_URL = "ec2-54-218-218-2.us-west-2.compute.amazonaws.com/data/"
REC_BASE_URL = "https://s3.amazonaws.com/rec_product_images/"

@csrf_exempt
def updateRecVector(user_id):
	TOP_PERCENTILE = 1.0
	THRESHOLD = 0.0
	
	# first check if the user already has a rec queued up
	if Notification.objects.get(user=user_id).is_ready:
		return True
	
	current_user = User.objects.get(pk=user_id)
	url = PROCESSING_URL + "generaterecmodel/" + user_id + "/"
	r = requests.post(url)
	
	new_recs = json.loads(r.text)
	# list of tuples 
	# determine if  there are any unique ones
	all_rec_ids = list(Recommendations.objects.filter(user=user_id).values_list('rec', flat=True))
	limit = len(new_recs) * TOP_PERCENTILE
	is_ready = False
	for i in range(limit):
		if new_recs[i][0] not in all_rec_ids:
			if new_recs[i][2] > THRESHOLD:
				is_ready = True
				rec = new_recs[i][2]

	# determine if the notification is ready and return True or False				
	notif = Notification.objects.get(user=user_id)
	if is_ready:
		Recommendation.objects.create(user=user_id, rec = rec, delivered = False)
		notif.is_ready = True
		notif.last_rec_update = datetime.datetime.now()
		notif.save()
		return True
	else:	
		notif.last_rec_update = datetime.datetime.now()
		notif.save()
		return False

@csrf_exempt
def getRecList(request, user_id):
	current_user = User.objects.get(pk=user_id)
	recs = Recommendation.objects.filter(user=current_user)
	data = []
	for user_rec in recs:
#		url = REC_BASE_URL + user_rec.rec.url
               	url = user_rec.rec.url
		data.append({"level": 1, "id": user_rec.id, "url": url, "text": user_rec.rec.text})
	data.reverse()
	response = HttpResponse(json.dumps(data), mimetype='application/json')
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1000"
	response["Access-Control-Allow-Headers"] = "*"
	return response

@csrf_exempt
def getNewRec(request, user_id):
#	return HttpResponse(json.dumps({"url": "https://s3.amazonaws.com/pave_training_images/Emma-Watson.jpg", "text": "TEST REC"}), mimetype="application/json")
	new_rec_iterator = Recommendation.objects.filter(user=user_id).filter(delivered=False)
	if (not new_rec_iterator):
		# get something from feel good rec
		return HttpResponse(json.dumps({"error": "no insight available"}), mimetype="application/json")
	new_rec = new_rec_iterator[0]
	new_rec.delivered = True
	new_rec.save()
	#return HttpResponse(json.dumps({"url": "www.google.com", "text": "THIS IS ONE FOR GOOGLE"}), mimetype="application/json")
	return HttpResponse(json.dumps({"url": new_rec.rec.url, "text": new_rec.rec.text}), mimetype="application/json")

@csrf_exempt
def agreeWithRec(request, user_id):
	if request.method == 'POST':
		rec = Recommendation.objects.get(pk = request.POST["rec_id"])
		if "agree" in json.dumps(request.POST):
			rec.agree = True
		else:
			rec.agree = False
		rec.save()
		return HttpResponse(json.dumps({"response": "ok"}), mimetype='application/josn')
	else:
		return HttpResponse("Not a POST")
