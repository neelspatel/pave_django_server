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
from data.models import Product
from data.models import User
from data.models import UserForm
from data.models import FeedObject
from data.models import Answer
from data.models import ListField
from data.models import TrendingObject
from data.models import ProductType
from data.models import Notification
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
from process_images import process_image

PROCESSING_URL = "ec2-54-218-218-2.us-west-2.compute.amazonaws.com/data/"

@csrf_exempt
def updateRecVector(user_id):
	try:
		current_user = User.objects.get(pk=user_id)
		url = PROCESSING_URL + "updaterecvector/" + user_id + "/"
		r = requests.post(url)
		notif, created = Notification.objects.get_or_create(user = User.objects.get(pk=user_id))
		notif.last_rec_update = datetime.datetime.now()
		notif.save()
		return True
	except:
		return False

	
