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
from data.models import QuestionObject
from django.forms.models import model_to_dict
from random import randint
from random import choice
import random
import datetime
import requests
import itertools
from collections import Counter
from data.notif_views import addNotification
from data.views import updateQuestionObjectQueue

def getGender(questionObject):
	text =  questionObject.currentQuestion.type.text
	if text.endswith("_female"):
		return "female"
	elif text.endswith("_male"):
		return "male"
	else: 
		return None

@csrf_exempt
def getGroupListQuestions(request, user_id):
	if request.method == "POST":	
		NUM_OBJECTS = 100	
		current_user = User.objects.get(pk=user_id)
		group = json.loads(request.POST["group"])
		genders = {}
		names = {}
		males = []
		females = []
		for friend in group:
			# get the gender	
			index = current_user.friends.index(int(friend))
			gender = current_user.genders[index]
			name = current_user.names[index]
			names[friend] = name
			genders[friend] = gender
			if gender == "male":
				males.append(friend)
			else:
				females.append(friend)


		no_males = False
		no_females = False
		if (len(males) == 0):
			no_males = True
		if (len(females) == 0):
			no_females = True

		#get all feed items by friends
		# get Question Objects
		num_q_objects = QuestionObject.objects.filter(toUser=current_user).count()
		if num_q_objects < NUM_OBJECTS:
			q_objects = updateQuestionObjectQueue(current_user, NUM_OBJECTS)
		else:
			q_objects = QuestionObject.objects.filter(toUser=current_user)[:NUM_OBJECTS]
		
		list_question_objects = []
		for q in q_objects:
			# randomly pick a friend from the group 
			# how to get the gender of the friend?
			q_gender = getGender(q)
			if q_gender:
				if q_gender == "male":
					if (no_males):
						continue
					rand_friend = choice(males)
				else:
					if (no_females):
						continue
					rand_friend = choice(females)	

			else:
				rand_friend = choice(group)
			
			
			try:
				question_text = q.currentQuestion.text.replace("%n", current_friend["name"].split()[0])
			except:
				question_text = q.currentQuestion.text



								
			json_q = {
				"fbFriend1": [], 
				"fbFriend2": [], 
				"product1Count": q.product1Count, 
				"product2Count": q.product2Count, 
				"currentQuestion": q.currentQuestion.id,
				"name": names[rand_friend],
				"product1": q.product1.id,
				"product2": q.product2.id,
				"image1": q.image1,
				"image2": q.image2,
				"friend": str(rand_friend),
				"questionText": question_text
			}
			list_question_objects.append(json_q)
			# delete the q_object
			q.delete()

		response = HttpResponse(json.dumps(list_question_objects), mimetype='application/json')
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response


