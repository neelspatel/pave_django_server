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
import data.rec_views as rec_utils

@csrf_exempt
def getNotifications(request, user_id):
	current_user = User.objects.get(pk = user_id)
	try:
		notification = Notification.objects.get(user=current_user)
		data = {"status_score": notification.status_score, "answers": notification.number_answers, "ug_answers": notification.number_ug_answers, "recs": notification.number_recs}
	except Notification.DoesNotExist:
		data = {"status_score": 0, "answers": 0, "ug_answers": 0, "recs": 0}
	
	#data = {"answers": 4, "ug_answers": 5, "recs": 12}	
	
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


def updateNotification(user, notif_type, reset=False):
	current_user = user
	notif = notif_type[0]
	notification = Notification.objects.get(user=current_user)
	if reset:			
		setattr(notification, notif, 0)
	else:			
		amt = notif_type[1]
		setattr(notification, notif, F(notif) + amt)

	# update status score takes care of passing this in	
	if notif == "answers_since_update":
		if ((notification.answers_since_update % 5) == 0 and (not notification.rec_ready)):
			rec_ready = rec_utils.updateRecVector(user.pk)
			if rec_ready:
				notification.rec_ready = True
	notification.save()
	return True

# Use this function to update a status score
def updateStatusScore(user, action):
	# on a scale to 100
	stages = {"early": 20, "middle": 50, "danger": 80, "final": 90} 
	actions = {"training": 0, "answer_recieved": 1, "answer_given": 2}	
	rate = (15, 10, 3)

	# if an answer was given about this user 
	if action in ["training", "answer_recieved"]:
		updateNotification(user, ("answers_since_update", 1))

	notif = Notification.objects.get(user=user)
	old_status_score = notif.status_score
	pre_scale = rate[actions[action]] + old_status_score

	if notif.rec_ready:
		scale = 4
	else:
		if pre_scale > stages["final"]:
			scale = 0.0
		elif pre_scale > stages["danger"]:
			scale = 0.1
		elif pre_scale > stages["middle"]:
			scale = 1
		else:
			scale = 2
	increase = int(scale * rate[actions[action]])	
	upateNotification(user, ("status_score", increase))

