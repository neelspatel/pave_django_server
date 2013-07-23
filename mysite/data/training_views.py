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
from collections import Counter
from data.views import random_combinations

UG_IMAGES_BASE_URL = "https://s3.amazonaws.com/ug_product_images/"
TRAINING_IMAGES_BASE_URL = "https://s3.amazonaws.com/pave_training_images/"
PRODUCT_IMAGES_BASE_URL = "https://s3.amazonaws.com/pave_product_images/"

# THIS IS FOR TRAINING PURPOSES
@csrf_exempt
def getRecsListQuestions(request, user_id):
	jock = {"name": "Vin Diesel", "id": "10150153748568313"}
	science = {"name": "Bill Nye", "id": "48947135361"}
	artsy = {"name": "James Franco", "id": "339468806098340"}
	list_choices = [jock, science, artsy]

	current_user = User.objects.get(pk=user_id)
	list_friends_objects = []
	num_new_objects = 100

	for x in range(num_new_objects):
		
		current_friend = choice(list_choices)		
		name = current_friend["name"]

		#gets a random quesiton
        	num_questions = Question.objects.count() -1
        	currentQuestion = Question.objects.all()[randint(0,num_questions)]

        	#gets the type we're dealing with
        	current_type = currentQuestion.type

        	#now gets two random products in that type
        	num_products = current_type.count - 1
        	index1 = randint(1, num_products)  
        	index2 = randint(1, num_products) -1 
       		if index1 == index2: index2 = num_products

       		currentProduct1 = Product.objects.get(type = current_type, idInType = index1)
	        currentProduct2 = Product.objects.get(type = current_type, idInType = index2)

		old_objects = FeedObject.objects.filter(forUser=current_friend, product1=currentProduct1, product2=currentProduct2, currentQuestion=currentQuestion) 

		current_object = {}
                if len(old_objects)==0:
 #                       current_object = FeedObject()
                        #creates the object to save it in the dictionary
                        current_object['product1'] = currentProduct1.id
                        current_object['product2'] = currentProduct2.id
                        current_object['image1'] = currentProduct1.fileURL
                        current_object['image2'] = currentProduct2.fileURL
                        current_object['fbFriend1'] = []
                        current_object['fbFriend2'] = []
                        current_object['product1Count'] = 0
                        current_object['product2Count'] = 0
                        current_object['currentQuestion'] = currentQuestion.id
                        current_object['questionText'] = currentQuestion.text
                else:
#                        current_object = old_objects[0]
                        current_object['product1'] = old_objects[0].product1.id
                        current_object['product2'] = old_objects[0].product2.id
                        current_object['image1'] = old_objects[0].image1
                        current_object['image2'] = old_objects[0].image2
                        current_object['fbFriend1'] = old_objects[0].fbFriend1
                        current_object['fbFriend2'] = old_objects[0].fbFriend2
                        current_object['product1Count'] = old_objects[0].product1Count
                        current_object['product2Count'] = old_objects[0].product2Count
                        current_object['currentQuestion'] = old_objects[0].currentQuestion.id
                        current_object['questionText'] = old_objects[0].questionText

		try:
			current_object['questionText'] = current_object['questionText'].replace("%n", name.split()[0])
		except:
			current_object['questionText'] = current_object['questionText']

		current_object['name'] = name
		current_object['friend'] = current_friend["id"]
		
		list_friends_objects.append(current_object)

	response = HttpResponse(json.dumps(list_friends_objects), mimetype='application/json')
	response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response



@csrf_exempt
def getTrainingListQuestions(request, user_id):
	current_user = User.objects.get(pk=user_id)
	profile = json.loads(current_user.profile)
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
			p1_url = TRAINING_IMAGES_BASE_URL + product1.fileURL 
			p2_url = TRAINING_IMAGES_BASE_URL + product2.fileURL
			json_q = {
				"currentQuestion":question.id,
				"name": name,
				"product1": product1.id,
				"product2": product2.id,
				"image1": p1_url,
				"image2": p2_url,
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
		user = User.objects.get(pk=json_ug_answer["userID"]),
		chosenUGProduct = TrainingProduct.objects.get(pk=json_ug_answer["chosen"]),
		wrongUGProduct = TrainingProduct.objects.get(pk=json_ug_answer["wrong"]),
		question = TrainingQuestion.objects.get(pk=json_ug_answer["question"])
	)



