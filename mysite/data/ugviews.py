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
from data.models import UserGeneratedQuestion, UserGeneratedProduct, UserGeneratedAnswer, QuestionQueue
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

def uploadUGProductImage(request):
	if request.method == 'POST':
		request.POST["product1_filename"]
		request.POST["product2_filename"]
		request.POST["product1_url"]
		request.POST["product2_url"]
		
		# use process_images.py

	return HttpResponse("Not a post request")
@csrf_exempt
def createUGQuestion(request, user_id):
	current_user = User.objects.get(pk=user_id)
	
	# create the new User Generated Question, User Generated Products
	# deal with the uploaded images 

	if request.method == 'POST':
		# need url for product 1, url for product 2, description for product1/2, question text, 
		p1_url = request.POST['product1_url']
		p2_url = request.POST['product2_url']
		url = '54.244.251.104/uploadugproduct'
		p1_filename = user_id + "_1_%s.jpg" % datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
		p2_filename = user_id + "_2_%s.jpg" % datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
		r = requests.post(url, data = {"product1_filename": p1_filename, "product2_filename": p2_filename, "product2_url": p2_url, "product1_url": p1_url})
				
		# add to all of friends question queues 
		
	

