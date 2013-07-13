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

@csrf_exempt
def getNotifications(request, user_id):
	current_user = User.objects.get(pk = user_id)
	try:
		notification = Notification.objects.get(user=current_user)
		data = {"status_score": notification.status_score, "answers": notification.num_answers, "ug_answers": notification.num_ug_answers, "recs": notification.num_recs}
	except Notification.DoesNotExist:
		data = {"status_score": 0, "answers": 0, "ug_answers": 0, "recs": 0}
	
	# delete notification
	notification.delete()
	response = HttpResponse(json.dumps(data), mimetype="application/json")
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1000"
	response["Access-Control-Allow-Headers"] = "*"
	return response

def addNotification(user_id, notif):
	current_user = User.objects.get(pk=user_id)
	notif = notif_type[0]
	amt = notif_type[1]
	try:
		notification = Notification.objects.get(user=current_user)
		setattr(notification, notif, F(notif) + amt)
		notification.save()
	except:
		notification = Notification.objects.create(user = current_user)
		setattr(notification, notif, amt)
		notification.save()
	
