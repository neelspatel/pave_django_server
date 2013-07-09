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
from data.models import UserGeneratedQuestion, UserGeneratedProduct, UserGeneratedAnswer, UserGenerated, QuestionQueue
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


@csrf_exempt
def createUGQuestion(request, user_id):
	current_user = User.objects.get(pk=user_id)
	
	# create the new User Generated Question, User Generated Products
	# deal with the uploaded images 

	if request.method == 'POST':
	
		request.POST['data']
	

