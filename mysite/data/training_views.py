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

@csrf_exempt
def getTrainingListQuestions(request, user_id):
	current_user = User.objects.get(pk=user_id)
	profile = json.laods(current_user.profile)
	gender = profile['gender']
	name = profile['name']

	num_training_questions = 100
	q_list = TrainingQuestion.objects.filter(on = True).order_by("?")[:num_training_questions]
	
	# get unique product types
	p_types_counter = Counter([question.type for question in q_list])
	p_types_products = {}
	for p_type, count in p_types_counter.iteritems():
		 # get a list of pairs of two random products of the given product time
		curr_len = TrainingProduct.objects.filter(type=p_type).filter(on=True).count()
		curr_products = TrainingProduct.objects.filter(type=p_type).filter(on=True)
		p_types_products[p_type] = random_combinations(curr_products, curr_len, (num_training_questions * 2))
				
	if p_types_products:
		qq_list = []
		for question in q_list:
			# add a new object to the QuestionObject for the current user
			# package for the client			
			# deal with male female
			if question.type.text.endswith("_male"):
				question_gender = "male"
			elif question.type.text.endswith("female"):
				question_gender = "female"
			else:
				question_gender = None
			if question_gender:
				if not(question_gender == gender):
					continue

			
			p_tuple = p_types_products[question.type].pop(0)
			product1 = p_tuple[0]
			product2 = p_tuple[1]
					
			# get feed objects for count				
			try:
				question_text = question.text.replace("%n", name.split()[0])
			except:
				question_text = question.text
			json_q = {
				"currentQuestion":question.id,
				"name": q.aboutFriendName,
				"product1": product1.id,
				"product2": product2.id,
				"image1": product1.fileURL,
				"image2": product2.fileURL,
				"questionText": question_text
			}

			qq_list.append(json_q)
			response = HttpResponse(json.dumps(qq_list), mimetype='application/json')
			response["Access-Control-Allow-Origin"] = "*"
			response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
			response["Access-Control-Max-Age"] = "1000"
			response["Access-Control-Allow-Headers"] = "*"
        	return response

@csrf_exempt
def saveTrainingAnswer(json_ug_answer, user_id):
	TrainingAnswer.objects.create(
		user = User.objects.get(pk=json_ug_answer["userID"],
		chosenUGProduct = TrainingProduct.objects.get(pk=json_ug_answer["chosen"]),
		wrongUGProduct = TrainingProduct.objects.get(pk=json_ug_answer["wrong"]),
		question = TrainingQuestion.objects.get(pk=json_ug_answer["question"]
	)



