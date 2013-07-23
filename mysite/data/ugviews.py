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
from process_images import process_image

@csrf_exempt
def uploadUGProductImage(request):
	if request.method == 'POST':
		process_image(request.POST["product1_url"], request.POST["product1_filename"])
		process_image(request.POST["product2_url"], request.POST["product2_filename"])
		# use process_images.py
		return HttpResponse("looks like it worked")
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
		url = 'http://54.244.251.104/data/uploadugproduct'
		p1_filename = user_id + "_1_%s.jpg" % datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
		p2_filename = user_id + "_2_%s.jpg" % datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
			
		r = requests.post(url, data = {"product1_filename": p1_filename, "product2_filename": p2_filename, "product2_url": p2_url, "product1_url": p1_url})
		# create the new products
  
		product1 = UserGeneratedProduct.objects.create(fileURL = p1_filename, on = True, user = current_user, description = request.POST["product1_description"])				
	
		product2 = UserGeneratedProduct.objects.create(fileURL = p2_filename, on = True, user = current_user, description = request.POST["product2_description"])				
		ug_question = UserGeneratedQuestion.objects.create(user = current_user, text = request.POST["question_text"], product1 = product1, product2 = product2, on = True)
	 	
		for friend_id in current_user.friendsInApp:
			current_friend = User.objects.get(pk = friend_id)
			current_friend_qq = QuestionQueue.objects.create(toUser=current_friend, byUser=current_user, question=ug_question, on=True)				
		
		return HttpResponse(json.dumps({"data": "ok"}), mimetype="application/json")

	return HttpResponse("Not a POST request")
	
@csrf_exempt
def saveUGAnswer(json_ug_answer, user_id):
	UserGeneratedAnswer.objects.create(
		fromUser = User.objects.get(pk=json_ug_answer["userID"]),
		forUser = User.objects.get(pk=json_ug_answer["friend"]),
		chosenUGProduct = UserGeneratedProduct.objects.get(pk=json_ug_answer["chosen"]),
		wrongUGProduct = UserGeneratedProduct.objects.get(pk=json_ug_answer["wrong"]),
		question = UserGeneratedQuestion.objects.get(pk=json_ug_answer["question"])
	)


@csrf_exempt
def getUGQuestionsList(request, user_id):
	current_user = User.objects.get(pk=user_id)
	questions = UserGeneratedQuestion.objects.filter(user=current_user)
	data= []
	for q in questions:
		product1_filename = "https://s3.amazonaws.com/ug_product_images/" + q.product1.fileURL
		product2_filename = "https://s3.amazonaws.com/ug_product_images/" + q.product2.fileURL

		data.append({
					"question_text": q.text,
					"fbFriend1": q.fbFriend1,
					"fbFriend2": q.fbFriend2,
					"product_1": q.product1.id,
					"product_2": q.product2.id,
					"product_1_count": q.product1_count,
					"product_2_count": q.product2_count,
					"product_1_url": product1_filename,
					"product_2_url": product2_filename,
					"question_id": q.id
				})
	data.reverse()	
	response = HttpResponse(json.dumps(data), mimetype="application/json")
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1000"
	response["Access-Control-Allow-Headers"] = "*"
   	return response
