# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
from django.db.models import F
from django.core import serializers
from data.models import Notification, User
from notif_views import *

@csrf_exempt
def getNotifications(request, user_id):
	current_user = User.objects.get(pk = user_id)
	try:
		notification = Notification.objects.get(user=current_user)
		data = {"status_score": notification.status_score, "answers": notification.number_answers, "ug_answers": notification.number_ug_answers, "recs": notification.number_recs}
	except Notification.DoesNotExist:
		data = {"status_score": 0, "answers": 0, "ug_answers": 0, "recs": 0}
	data = {"answers": 4, "ug_answers": 5, "recs": 12}	
	
	# reset notification
	notification.number_answers = 0
	notification.number_ug_answers = 0
	notification.number_recs = 0
	notification.save()
	
	response = HttpResponse(json.dumps(data), mimetype="application/json")
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1000"
	response["Access-Control-Allow-Headers"] = "*"
	return response

def getScaleFactor(user_id):
	# what to do here
	return 1

def addNotification(user_id, notif):
	current_user = User.objects.get(pk=user_id)
	notif = notif_type[0]
	amt = notif_type[1]
	if notif == "status_score":
		factor = getScaleFactor(user_id)
		amt = amt * factor
	try:
		notification = Notification.objects.get(user=current_user)
		setattr(notification, notif, F(notif) + amt)
		notification.save()
	except:
		notification = Notification.objects.create(user = current_user)
		setattr(notification, notif, amt)
		notification.save()

# Use this function to update a status score
def updateStatusScore(user, action):
	# on a scale to 100
	stages = {"early": 20, "middle": 50, "danger": 80} 
	actions = {"training": 0, "": 1, "": 2}
	notif = Notification.objects.get(user=user)
	old_status_score = notif.status_score
	rate = (notif.rate_training, notif.rate_answer, notif.rate_others)
	pre_scale = rate[actions[action]] + old_status_score
	scale = notif.scale

	if notif.rec_ready:
		scale *= 2
	else:
		#if pre_scale > stages["danger"]:
		return 3
	


