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
from data.models import QuestionObject
from data.models import QuestionQueue
from data.models import UserGeneratedQuestion
from data.models import TrainingAnswer, TrainingQuestion, TrainingProduct
from django.forms.models import model_to_dict
from random import randint
from random import choice
from random import shuffle
import logging
import urllib
import random
import datetime
import calendar
import requests
import itertools
from collections import Counter
import httplib2
import oauth2
import time
from data.notif_views import updateNotification
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from top_friends import get_top_friends, get_friends, get_profile
import cPickle as pickle
import data.notif_views as notif_utils

UG_IMAGES_BASE_URL = "https://s3.amazonaws.com/ug_product_images/"
TRAINING_IMAGES_BASE_URL = "https://s3.amazonaws.com/pave_training_images/"
PRODUCT_IMAGES_BASE_URL = "https://s3.amazonaws.com/pave_product_images/"
APP_STORE_URL = "https://itunes.apple.com/us/app/side"

@csrf_exempt
def getAppStoreUrl(request):
	data = {"url": APP_STORE_URL}
	return HttpResponse(json.dumps(data), mimetype="application/json")

#for uploading a single file to s3 from a client somewhere
@csrf_exempt
def uploadImage(request):
	if request.FILES:
		filename = request.POST['name']
		con = S3Connection('AKIAJ5NFFKY3KUKBRTPQ','Z3heEPRxIvB0KXxLEaYZ69rpdOsQYXx2cwfprHpf')
		bucket = con.create_bucket('preparsedugproductimages')
		k = bucket.new_key(filename)
		k.key = filename
		k.set_metadata("Content-Type", "image/jpg")
		k.set_contents_from_string(request.FILES['fileupload'].read())
		k.set_acl('public-read')

		return HttpResponse("Files! ")
	return HttpResponse("No files")	


@csrf_exempt
def imagesearch(request):
        OAUTH_CONSUMER_KEY = "dj0yJmk9N2ZZbHpHMXRqNjdEJmQ9WVdrOVMxazNaelZuTmpRbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD05Zg--"
        OAUTH_CONSUMER_SECRET = "3fa34549164ea42f2c3afa510156a2311262f4e0"

	query = request.POST["query"]
	query = urllib.quote(query)

        url = "http://yboss.yahooapis.com/ysearch/images?q="+query
        consumer = oauth2.Consumer(key=OAUTH_CONSUMER_KEY,secret=OAUTH_CONSUMER_SECRET)
        params = {
                'oauth_version': '1.0',
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': int(time.time()),
        }

        oauth_request = oauth2.Request(method='GET', url=url, parameters=params)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, None)
        oauth_header=oauth_request.to_header(realm='yahooapis.com')

        # Get search results
        http = httplib2.Http()
        resp, content = http.request(url, 'GET', headers=oauth_header)

        #parses out the data
        try:
                parsed = json.loads(content)
                results = parsed["bossresponse"]["images"]["results"]


                response = HttpResponse(json.dumps(results), mimetype='application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"

                return response

        except:
                return HttpResponse("Sorry, error in getting the data")

@csrf_exempt
def checkimage(request):
	products = Product.objects.all()
	array = []
	for current in products:
		name = current.fileURL
		url = current.fileURL
		url = url.replace("+", "%2b")
		url = url.replace(" ", "+")
		url = "https://s3.amazonaws.com/pave_product_images/" + url
		array.append({"name":name, "url":url})
	return render_to_response('data/checkimage.html', {'data': array})

@csrf_exempt
def rebase(request):
    for current in ProductType.objects.all():
        current.count = 0
        current.save()

    for current in Product.objects.all():
        current.save()

    return HttpResponse()

@csrf_exempt
def index(request):
	a = pickle.load(open("test.p", 'rb'))
	return HttpResponse("Hey, you're at the index for views in data " + str(a["data"]))

@csrf_exempt
def numberOfNewObjects(request, user_id, time_since):
	count = FeedObject.objects.filter(forUser = user_id, updatedAt__gte=(time_since)).count()

#		latest = FeedObject.objects.filter(forUser = user_id).latest('updatedAt').updatedAt.utctimetuple()
#	if count != 0:
	try:
		most_recent = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
#		most_recent = calendar.timegm(FeedObject.objects.filter(forUser = user_id).latest('updatedAt').updatedAt.utctimetuple())
	except:
		most_recent = 0
#	else:
#		most_recent = calendar.timegm(datetime.datetime.utcnow().utctimetuple())	
	return HttpResponse(json.dumps({'count': count, 'last':most_recent}), mimetype='application/json')

@csrf_exempt
def getProfileStats(request, user_id):
        vote_count = Answer.objects.filter(fromUser = user_id).count()
	answer_count = Answer.objects.filter(forFacebookId = user_id).count()
	ug_question_count = UserGeneratedQuestion.objects.filter(user = user_id).count()
	level = User.objects.get(pk=user_id).level	
	data = {"vote_count": vote_count, "answer_count": answer_count, "ug_question_count": ug_question_count, "level": level}
        return HttpResponse(json.dumps(data), mimetype='application/json')


@csrf_exempt
def numberOfAnswersGiven(request, user_id):
        count = Answer.objects.filter(fromUser = user_id).count()

#               latest = FeedObject.objects.filter(forUser = user_id).latest('updatedAt').updatedAt.utctimetuple()
#       if count != 0:
#        try:
#                most_recent = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
#               most_recent = calendar.timegm(FeedObject.objects.filter(forUser = user_id).latest('updatedAt').updatedAt.$
#        except:
#                most_recent = 0
#       else:
#               most_recent = calendar.timegm(datetime.datetime.utcnow().utctimetuple())        
        return HttpResponse(json.dumps([count]), mimetype='application/json')

@csrf_exempt
def numberOfAnswersGivenForJS(request, user_id):
	count = Answer.objects.filter(fromUser = user_id).count()
	response = HttpResponse(json.dumps([count]), mimetype='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
	return response

def hasAnsweredTrending(user, product_1, product_2):
	if Answer.objects.filter(fromUser = user).filter(forFacebookId = user.pk).filter(Q(chosenProduct = product_1) | Q(chosenProduct= product_2)).filter(Q(wrongProduct=product_1) | Q(wrongProduct=product_2)).count() > 0:
		return True
	return False		


@csrf_exempt
def getTrendingObjects(request, user_id):
	current_user = User.objects.get(pk=user_id)

	# all of the types in the current trending objects
	unique_types = TrendingObject.objects.values_list('type', flat=True).distinct()
	# placeholeder to return
	generated_objects = []
	for cur_type in unique_types:
		current_list = {}
		current_list[cur_type] = []
		cur_objects = TrendingObject.objects.filter(type = cur_type)
		for cur_object in cur_objects:
			if (not hasAnsweredTrending(current_user, cur_object.product1_id, cur_object.product2_id)):
				cur_object.forUser = user_id
				cur_object.question_text = cur_object.question_text.replace("%n", "you")
				current_list[cur_type].append(model_to_dict(cur_object))
		to_delete = []
		for p_type, object_list in current_list.iteritems():
			if len(object_list) == 0:
				to_delete.append(p_type)
		for to_d in to_delete:
			current_list.pop(to_d, None)
		if current_list:
			generated_objects.append(current_list)

	response = HttpResponse(json.dumps((generated_objects)), mimetype='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response



@csrf_exempt
def getAllAnswers(request, user_id):
	#first thing is get the current user
#	current_user = User.objects.get(pk=user_id)
	
	#now get all answers for that user
	all_answers = Answer.objects.prefetch_related().filter(forFacebookId = user_id)

	#now just return all of those answers
	response = HttpResponse(serializers.serialize("json", list(all_answers)), mimetype='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

@csrf_exempt
def getListQuestions(request, user_id):
        # do some cool shit here 

        #get all feed items by friends
        current_user = User.objects.get(pk=user_id)
        friends_objects = FeedObject.objects.filter(forUser__in=current_user.friendsInApp)
        #friends_objects = friends_objects.filter(product1Count__in=[1,2,3]) 
        #friends_objects = friends_objects.filter(product2Count__in=[1,2,3])[:50]
        friends_objects = friends_objects[:50]
        num_friends_objects = friends_objects.count()
        list_friends_objects = list(friends_objects)

        #now creates the number of questions by hand
        num_new_objects = 100 - num_friends_objects
        for x in range(num_new_objects):
                current_friend = choice(current_user.friends)

                #gets a random quesiton
                num_questions = Question.objects.count() -1
                currentQuestion = Question.objects.all()[randint(0,num_questions)]

                #gets the type we're dealing with
                current_type = currentQuestion.type

                #now gets two random products in that type
                num_products = current_type.count - 1
                index1 = randint(1, num_products)
                index2 = randint(1, num_products - 1)
                if index1 == index2: index2 = num_products

                currentProduct1 = Product.objects.get(type = current_type, idInType = index1)
                currentProduct2 = Product.objects.get(type = current_type, idInType = index2)

                old_objects = FeedObject.objects.filter(forUser=current_friend, product1=currentProduct1, product2=currentProduct2, currentQuestion=currentQuestion)

                if len(old_objects)==0:
                        current_object = FeedObject()
                        #creates the object to save it in the dictionary
                        current_object.forUser = current_friend
                        current_object.product1 = currentProduct1
                        current_object.product2 = currentProduct2
                        current_object.image1 = currentProduct1.fileURL
                        current_object.image2 = currentProduct2.fileURL
                        current_object.fbFriend1 = []
                        current_object.fbFriend2 = []
                        current_object.product1Count = 0
                        current_object.product2Count = 0
                        current_object.currentQuestion = currentQuestion
                        current_object.questionText = currentQuestion.text
#			current_object.questionText = "New here"
                else:
                        current_object = old_objects[0]

#		current_object.questionText = current_user.names[current_user.friends.index(current_friend)]
#		current_object.questionText = "New q"

                list_friends_objects.append(current_object)

#       json_data = serializers.serialize("json", list_friends_objects)

        combined = []
        for current_object in list_friends_objects:
#               combined.append(current_object)
                index = random.randint(0,len(current_user.friends) - 1)
                friend = current_user.friends[index]
                name = current_user.names[index]
                data = {'object': current_object, 'friend': {'id':friend, 'name':name}}
                combined.append(data)

        response = HttpResponse(serializers.serialize("json", list_friends_objects), mimetype='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
	response["Access-Control-Allow-Headers"] = "*"
        return response

def random_combinations(iterable, length, num):
	pool = tuple(iterable)
	result = []
	for i in range(num):
		indices = sorted(random.sample(xrange(length), 2))
		result.append(list(pool[i] for i in indices))
	return result

# get the friends facebook id and name
# STILL DONE WITH MUTUAL FRIENDS UPDATE TO ACCOUNT FOR NEW PROBS
def getFriendWithValidName(current_user, gender = None):
	MUTUAL_FRIEND_PROB = 0.8
	name = ""
	while name == "":
		if len(current_user.friends) < 100:	
			index = random.randint(0,len(current_user.friends) - 1)
		else:
			decision = random.random()
			if decision < MUTUAL_FRIEND_PROB:
				index = random.randint(0, 100-1)
			else:
				index = random.randint(100,len(current_user.friends) - 1)
		if gender:
			if not (gender == str(current_user.genders[index])):
				name = ""
				continue
		current_friend = str(current_user.friends[index])
		name = current_user.names[index]
		#checks if it is a valid name (in a very hackish way)
		if name != name.decode('utf8'):
			name = ""

	return {"name": name, "facebook_id": current_friend}

# Top Friends method
@csrf_exempt
def getFriendWithValidNameTopFriends(current_user, gender = None):
	MUTUAL_FRIEND_PROB = 0.8
	TOP_FRIEND_PROB = 0.9
	name = ""
	while name == "":
		if len(current_user.topFriends) == 0:
			if len(current_user.friends) > 100:
				decision = random.random()
				if decision < MUTUAL_FRIEND_PROB:
					index = random.randint(0, 100-1)
				else:
					index = random.randint(100,len(current_user.friends) - 1)		
			else:	
				index = random.randint(0,len(current_user.friends) - 1)
		else:
			decision = random.random()
			if decision < TOP_FRIEND_PROB:
				top_friends_index = random.randint(0, len(current_user.topFriends) - 1)
				index = current_user.friends.index(current_user.topFriends[top_friends_index])
			else:
				index = random.randint(0,len(current_user.friends) - 1)
				
		# check gender
		if gender:
			if not (gender == str(current_user.genders[index])):
				name = ""
				continue
		
		current_friend = str(current_user.friends[index])
		name = current_user.names[index]
		#checks if it is a valid name (in a very hackish way)
		try:
			if (name != name.decode('utf8')):
				name = ""
		except:
			name = ""
	return {"name": name, "facebook_id": current_friend}


def updateQuestionObjectQueue(current_user, count=100, replace=False):
	# maybe very slow
	q_list = Question.objects.filter(on = True).order_by("?")[:count]
	# get unique product types
	p_types_counter = Counter([question.type for question in q_list])
	p_types_products = {}
	for p_type, count in p_types_counter.iteritems():
		 # get a list of pairs of two random products of the given product time
		curr_len = Product.objects.filter(type=p_type).filter(on=True).count()
		curr_products = Product.objects.filter(type=p_type).filter(on=True)
		p_types_products[p_type] = random_combinations(curr_products, curr_len, (count * 2))
	
		
	if p_types_products:
		# delete all of the questions for this user
		if replace:
			QuestionObject.objects.filter(toUser=current_user).delete()

		male_friends = []
		female_friends = []
		for i in range(len(current_user.friends)):
			if current_user.genders[i] == "male":
				male_friends.append(current_user.friends[i])
			else:
				male_friends.append(current_user.friends[i])
				
		# we got a non-empty dictionary
		qq_list = []
		for question in q_list:
			# add a new object to the QuestionObject for the current user
			# package for the client			
			# deal with male female
			if question.type.text.endswith("_male"):
				if (len(male_friends) == 0):
					continue
				current_friend = getFriendWithValidNameTopFriends(current_user, "male")
			elif question.type.text.endswith("_female"):
				if(len(female_friends) == 0):
					continue 
				current_friend = getFriendWithValidNameTopFriends(current_user, "female")
			else:
				current_friend = getFriendWithValidNameTopFriends(current_user)
			p_tuple = p_types_products[question.type].pop(0)
			product1 = p_tuple[0]
			product2 = p_tuple[1]
					
			# get feed objects for count
			old_objects = FeedObject.objects.filter(forUser=current_friend, product1=product1, product2=product2, currentQuestion=question) 
                	p1_count = 0
			p2_count = 0
			if not(len(old_objects)==0):
				p1_count = old_objects[0].product1Count
				p2_count = old_objects[0].product2Count
			
			try:
				question_text = question.text.replace("%n", current_friend["name"].split()[0])
			except:
				question_text = question.text

			q_q = QuestionObject.objects.create(
				toUser = current_user,
				aboutFriend = current_friend["facebook_id"],
				aboutFriendName = current_friend["name"],
				product1 = product1,
				product2 = product2,
				image1 = product1.fileURL,
				image2 = product2.fileURL,
				currentQuestion = question,
				questionText = question_text,
				product1Count = p1_count,
				product2Count = p2_count
			)	
			qq_list.append(q_q)
		return qq_list

#
@csrf_exempt
def newGetListQuestions(request, user_id):
	NUM_OBJECTS = 100	
	NUM_UG_QUESTIONS = 20
	#get all feed items by friends
	current_user = User.objects.get(pk=user_id)

	# get User Generated Questions from Question Queue
	has_ug_questions = False
	ug_question_queue_count = QuestionQueue.objects.filter(toUser = current_user).count()
	if ug_question_queue_count > 0:
		has_ug_questions = True
		# we have user generated questions for this user
		if ug_question_queue_count < 20:
			NUM_UG_QUESTIONS = ug_question_queue_count
		ug_questions = QuestionQueue.objects.filter(toUser = current_user).order_by("id")[:NUM_UG_QUESTIONS]
	
	# determine how many questions that we need to get 
	num_questions = NUM_OBJECTS - NUM_UG_QUESTIONS
	# get Question Objects
	num_q_objects = QuestionObject.objects.filter(toUser=current_user).count()
	if num_q_objects < NUM_OBJECTS:
		q_objects = updateQuestionObjectQueue(current_user, num_questions)
	else:
		q_objects = QuestionObject.objects.filter(toUser=current_user)[:num_questions]


	questions = list(q_objects)
	if (has_ug_questions):
		questions  = list(ug_questions) + questions
		shuffle(questions)
	
	
	list_question_objects = []
	for q in questions:
		# determine if q is user_generated
		if type(q) == QuestionObject:		
			p1_url = PRODUCT_IMAGES_BASE_URL + q.image1
			p2_url = PRODUCT_IMAGES_BASE_URL + q.image2
			json_q = {
				"isUG": False,
				"fbFriend1": [], 
				"fbFriend2": [], 
				"product1Count": q.product1Count, 
				"product2Count": q.product2Count, 
				"currentQuestion": q.currentQuestion.id,
				"name": q.aboutFriendName,
				"product1": q.product1.id,
				"product2": q.product2.id,
				"image1": p1_url,
				"image2": p2_url,
				"friend": q.aboutFriend,
				"questionText": q.questionText
			}
		else:
			p1_url = UG_IMAGES_BASE_URL + q.question.product1.fileURL
			p2_url = UG_IMAGES_BASE_URL + q.question.product2.fileURL
			json_q = {
				"isUG": True,
				"fbFriend1": [],
				"fbFriend2": [],
				"product1Count": q.question.product1_count,
				"product2Count": q.question.product2_count,
				"currentQuestion": q.question.id,
				"name": json.loads(q.byUser.profile)["name"],
				"product1": q.question.product1.id,
				"product2": q.question.product2.id,
				"image1": p1_url,
				"image2": p2_url,
				"friend": q.byUser.facebookID,
				"questionText": q.question.text
			}
		
		list_question_objects.append(json_q)
		q.delete()

	response = HttpResponse(json.dumps(list_question_objects), mimetype='application/json')
	response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

@csrf_exempt
def getListQuestionsForGroup(request, user_id):	
	return HttpResponse("Not Implemented", status=500)

@csrf_exempt
def updateTopFriends(request, user_id):
	if request.method == 'POST':
		try:
			current_user = User.objects.get(pk=user_id)
		except:
			return HttpResponse("Not a valid user")
		
		top_friends = json.loads(request.POST["top_friends"])
		current_user.topFriends = top_friends
		current_user.save()
		return HttpResponse("updated top friends")
	else:
		return HttpResponse("Not a POST request")

@csrf_exempt
def getListQuestionsNew(request, user_id):
	# do some cool shit here 
	
	#get all feed items by friends
	current_user = User.objects.get(pk=user_id)
#	friends_objects = FeedObject.objects.filter(forUser__in=current_user.friendsInApp)
#	return HttpResponse(friends_objects.count())
	#friends_objects = friends_objects.filter(product1Count__in=[1,2,3]) 
	#friends_objects = friends_objects.filter(product2Count__in=[1,2,3])[:50]
#	friends_objects = friends_objects[:50]
#	num_friends_objects = friends_objects.count()
#	all_friends_objects = list(friends_objects)
	list_friends_objects = []

#	for old_object in all_friends_objects:
#		current_object = {}
#		current_object['product1'] = old_object.product1.id
#               current_object['product2'] = old_object.product2.id
#                current_object['image1'] = old_object.image1
#                current_object['image2'] = old_object.image2
#                current_object['fbFriend1'] = old_object.fbFriend1
#                current_object['fbFriend2'] = old_object.fbFriend2
#                current_object['product1Count'] = old_object.product1Count
#                current_object['product2Count'] = old_object.product2Count
#                current_object['currentQuestion'] = old_object.currentQuestion.id
#                current_object['questionText'] = old_object.questionText
		
#		index = random.randint(0,len(current_user.friends) - 1)
#                friend = str(current_user.friends[index])
#                name = current_user.names[index]

#                current_object['name'] = name
#                current_object['friend'] = friend

#		list_friends_objects.append(current_object)

#	return HttpResponse(json.dumps(list_friends_objects))

	#now creates the number of questions by hand
#	num_new_objects = 100 - num_friends_objects
	num_new_objects = 100
	for x in range(num_new_objects):
#		current_friend = choice(current_user.friends)

		name = ""
		while name == "":
			if len(current_user.friends) < 100:	
				index = random.randint(0,len(current_user.friends) - 1)
			else:
				decision = random.random()
				if decision < 0.8:
					index = random.randint(0, 100-1)
				else:
					index = random.randint(100,len(current_user.friends) - 1)

	                current_friend = str(current_user.friends[index])
        	        name = current_user.names[index]
			#checks if it is a valid name (in a very hackish way)
			if name != name.decode('utf8'):
				name = ""
			

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
		current_object['friend'] = current_friend
		
		list_friends_objects.append(current_object)

	response = HttpResponse(json.dumps(list_friends_objects), mimetype='application/json')
	response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

@csrf_exempt
def getFeedObject(request, feed_object_id):
	try:
		result = FeedObject.objects.get(pk=feed_object_id)
		response = HttpResponse(serializers.serialize("json", [result]), mimetype='application/json')		
	except:
		response = HttpResponse(serializers.serialize("json", []), mimetype='application/json')

	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*" 
	return response

@csrf_exempt
def getInsight(request, user_id):
	try:
		result = Recs.object.filter(user_id = User.objects.get(pk = user_id))
	except:
		response = HttpResponse(serializers.serialize("json", []), mimetype= "application/json")

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
	# - have score for each product type for the user 



@csrf_exempt
def getAllFeedObjects(request, user_id):
        ids = []

	objects_to_return = []
	all_feed_objects = FeedObject.objects.filter(forUser = user_id)
	for current_object in all_feed_objects:
		for friend in current_object.fbFriend1:
			p1_url = PRODUCT_IMAGES_BASE_URL + current_object.product1.fileURL
			p2_url = PRODUCT_IMAGES_BASE_URL + current_object.product2.fileURL
			objects_to_return.append(
				{
					"question":current_object.questionText, 
					"questionID":current_object.currentQuestion.id,
					"friend":friend, 
					"chosenProduct": p1_url, 
					"chosenProductID": current_object.product1.id,
					"otherProductID": current_object.product2.id,
					"otherProduct": p2_url
				})
		for friend in current_object.fbFriend2:
			p1_url = PRODUCT_IMAGES_BASE_URL + current_object.product1.fileURL
			p2_url = PRODUCT_IMAGES_BASE_URL + current_object.product2.fileURL
                        objects_to_return.append(
				{
					"question":current_object.questionText, 
					"questionID":current_object.currentQuestion.id,
					"friend":friend, 
					"chosenProduct": p1_url,
					"chosenProductID": current_object.product1.id,
                                        "otherProductID": current_object.product2.id,
					"otherProduct": p2_url,

				})

	
	name = json.loads(User.objects.get(pk=user_id).profile)['name']
	
	for current_object in objects_to_return:
		current_object['question'] = current_object['question'].replace("%n", name.split()[0])
		
	objects_to_return.reverse()
	
	response = HttpResponse(json.dumps(objects_to_return), mimetype = 'application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

@csrf_exempt
def getUser(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
		response = HttpResponse(serializers.serialize("json", [user]), mimetype='application/json')
	except:
                response = HttpResponse(serializers.serialize("json", []), mimetype='application/json')

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
		

#gets a random question, and returns two random products in that product type
@csrf_exempt
def randomQuestion(request):
	#gets a random quesiton
	num_questions = Question.objects.count() - 1	
	question = Question.objects.all()[randint(0,num_questions)]

	#gets the type we're dealing with
	current_type = question.type
	
	#now gets two random products in that type
	num_products = current_type.count - 1
	index1 = randint(0, num_products)
	index2 = randint(0, num_products - 1)
	if index1 == index2: index2 = num_products
	
	product1 = Product.objects.get(type = current_type, idInType = index1)
	product2 = Product.objects.get(type = current_type, idInType = index2)

	response = HttpResponse(serializers.serialize("json", [question, current_type, product1, product2]), mimetype='application/json')
	response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
	return response

@csrf_exempt
def detail(request):
	#try:
	#	#data_id is the call name, such as Sample_Call
	#	data = Data.objects.get(call=data_id)
	#except Data.DoesNotExist:
	#	raise Http404
	#return render(request, 'data/detail.html', {'data': data})
	#return HttpResponse("You're at call name %s." % data_id)
	
	#data_id is the call name, such as Sample_Call
	#data = Data.objects.get(call=data_id)
	#response = HttpResponse(serializers.serialize("json", [data]), mimetype='application/javascript')		
	#response["Access-Control-Allow-Origin"] = "*"  
	#response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
	#response["Access-Control-Max-Age"] = "1000"  
	#response["Access-Control-Allow-Headers"] = "*" 
	#return response

	return HttpResponse("Hey, you're at details in data")

@csrf_exempt
def changeAnswer(request):
        if request.method == 'POST':
		from_user = User.objects.get(pk = request.POST["id_facebookID"])
		forFacebookId = request.POST["id_forFacebookID"]
		
		is_user = False
		if User.objects.filter(pk=forFacebookId).exists():
			is_user = True			

		chosen_product_id = request.POST["id_chosenProduct"]
		wrong_product_id = request.POST["id_wrongProduct"]
		question_id = request.POST["id_question"]
		user_id = request.POST["id_facebookID"]

		if "isUG" in request.POST:
			# change the question count on the user generated question
			question = UserGeneratedQuestion.objects.get(pk=question_id)
			chosen_product = UserGeneratedProduct.objects.get(pk=chosen_product_id)
			wrong_product = UserGeneratedProduct.objects.get(pk=wrong_product_id)
			if (chosen_product == question.product1):
				question.product2_count -= 1
				try:
					question.fbFriend2.pop(user_id)
				except:
					# bad things happened
					pass
				question.fbFriend1.append(user_id)
			else:
				question.product1_count -= 1
				try:
					question.fbFriend1.pop(user_id)
				except:
					# bad things happened
					pass
				question.fbFriend2.append(user_id)
			question.save()

			# delete the old answer
			UserGeneratedAnswer.objects.filter(fromUser = from_user).filter(forUser=User.objects.get(pk=forFacebookId)).filter(question=question).filter(chosenUGProduct = wrong_product, wrongUGProduct=chosen_product).delete()
			
			# create the new answer
			obj = UserGeneratedAnswer.objects.create(
				fromUser = from_user,
				forUser = User.objects.get(pk=forFacebookId),
				chosenUGProduct = chosen_product, 
				wrongUGProduct = wrong_product, 
				question = question
			)

			notif_utils.updateNotification(forFacebookId, ("number_ug_answers", 1))

		elif "is_training" in request.POST:
			obj = TrainingAnswer.objects.create(
				user = from_user,
				wrongProduct=  TrainingProduct.objects.get(pk=wrong_product_id),
				chosenProduct = TrainingProduct.objects.get(pk=chosen_product_id),
				question = TrainingQuestion.objects.get(pk=question_id)			
			)
			notif_utils.updateStatusScore(user, "training")
		else:
			
			if is_user:
				notif_utils.updateNotification(forFacebookId, ("number_answers", 1))
				notif_utils.updateStatusScore(forFacebookId, "answer_recieved")
			notif_utils.updateStatusScore(from_user, "answer_given")
			
			chosen_product = Product.objects.get(pk=chosen_product_id)
			wrong_product = Product.objects.get(pk=wrong_product_id)
			question = Question.objects.get(pk=question_id)

			feed_object = FeedObject.objects.filter(currentQuestion=question).filter(forUser=forFacebookId)[0]
			if (feed_object.product1 == chosen_product):
				feed_object.product2Count -= 1
				try:
					feed_object.fbFriend2.pop(user_id)
				except:
					pass
				feed_object.fbFriend1.append(user_id)

			else:
				feed_object.product1Count -= 1
				try:
					feed_object.fbFriend1.pop(user_id)
				except:
					pass
				feed_object.fbFriend2.append(user_id)
			feed_object.save()

			# delete the old answer			
			Answer.objects.filter(fromUser=from_user).filter(forFacebookId=forFacebookId).filter(question=question).filter(chosenProduct=chosen_product).filter(wrongProduct=wrong_product).delete()
		
			if "is_anonymous" in request.POST:
				anonymous_id = request.POST["is_anonymous"]	
				obj = Answer.objects.create(
					fromUser = from_user,
					forFacebookId = forFacebookId,
					chosenProduct = chosen_product,  
					wrongProduct = wrong_product,  
					question = question,
					anonymousUser = User.objects.get(pk=anonymous_id)
				)
			else:
				obj = Answer.objects.create(
					fromUser = from_user,
					forFacebookId = forFacebookId,
					chosenProduct = chosen_product,  
					wrongProduct = wrong_product,  
					question = question
				)


                response = HttpResponse(str(request.POST), mimetype = 'application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
        return HttpResponse("Not a POST request")

@csrf_exempt
def agreeWithAnswer(request, user_id):
	if request.method == 'POST':
		from_user = User.objects.get(pk=request.POST["id_facebookID"])
		forFacebookId = request.POST["id_forFacebookId"]

		chosen_product_id = request.POST["id_chosenProduct"]
		wrong_product_id = request.POST["id_wrongProduct"]
		question_id = request.POST["id_question"]

		notif_utils.updateStatusScore(from_user, "answer_recieved")
	
		obj = Answer.objects.create(
			fromUser = from_user,
			forFacebookId = forFacebookId,
			chosenProduct = Product.objects.get(pk=chosen_product_id),
			wrongProduct = Product.objects.get(pk=wrong_product_id),
			question = Question.objects.get(pk=question_id)
		)
		
		response = HttpResponse(str(request.POST), mimetype = 'application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
	return HttpResponse("Not a POST request")	
		
	

@csrf_exempt
def newAnswer(request):
        if request.method == 'POST':
		from_user = User.objects.get(pk = request.POST["id_facebookID"])
		forFacebookId = request.POST["id_forFacebookID"]
		
		is_user = False
		if User.objects.filter(pk=forFacebookId).exists():
			is_user = True			

		chosen_product_id = request.POST["id_chosenProduct"]
		wrong_product_id = request.POST["id_wrongProduct"]
		question_id = request.POST["id_question"]

		if "is_ug" in request.POST:
			obj = UserGeneratedAnswer.objects.create(
				fromUser = from_user,
				forUser = User.objects.get(pk=forFacebookId),
				chosenUGProduct = UserGeneratedProduct.objects.get(pk=chosen_product_id),
				wrongUGProduct = UserGeneratedProduct.objects.get(pk=wrong_product_id),
				question = UserGeneratedQuestion.objects.get(pk=question_id)
			)
			notif_utils.updateNotification(forFacebookId, ("number_ug_answers", 1))

		elif "is_training" in request.POST:
			obj = TrainingAnswer.objects.create(
				user = from_user,
				wrongProduct=  TrainingProduct.objects.get(pk=wrong_product_id),
				chosenProduct = TrainingProduct.objects.get(pk=chosen_product_id),
				question = TrainingQuestion.objects.get(pk=question_id)			
			)
			notif_utils.updateStatusScore(from_user, "training")
		else:
			if is_user:
				notif_utils.updateNotification(forFacebookId, ("number_answers", 1))
				notif_utils.updateStatusScore(forFacebookId, "answer_recieved")
			notif_utils.updateStatusScore(from_user, "answer_given")
				
			if "is_anonymous" in request.POST:
				anonymous_id = request.POST["is_anonymous"]	
				obj = Answer.objects.create(
					fromUser = from_user,
					forFacebookId = forFacebookId,
					chosenProduct =  Product.objects.get(pk=chosen_product_id),
					wrongProduct =  Product.objects.get(pk=wrong_product_id),
					question = Question.objects.get(pk=question_id),
					anonymousUser = User.objects.get(pk=anonymous_id)
				)
			else:
				obj = Answer.objects.create(
					fromUser = from_user,
					forFacebookId = forFacebookId,
					chosenProduct =  Product.objects.get(pk=chosen_product_id),
					wrongProduct =  Product.objects.get(pk=wrong_product_id),
					question = Question.objects.get(pk=question_id),
				)


                response = HttpResponse(str(request.POST), mimetype = 'application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
        return HttpResponse("Not a POST request")

@csrf_exempt
def batchCreateQuestions(request):
	if request.method == "POST":
		allQuestions = json.loads(request.POST["data"])
		for currentRow in allQuestions:
			p_type = ProductType.objects.get(text=currentRow["type"])
			if p_type:
				obj = Question.objects.get_or_create(
					type = p_type,
					text = currentRow["text"],
					on=True
				)
		response = HttpResponse(len(json.loads(request.POST["data"])), mimetype='application/json')
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = '1000'
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse("Request was not a POST")

@csrf_exempt
def batchCreateProducts(request):
	# to save a product we need product type
	
	debug =  HttpResponse(str(json.loads(request.POST["data"])), mimetype="application/json")
	debug["Access-Control-Allow-Origin"] = "*"
	debug["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	debug["Access-Control-Max-Age"] = '1000'
	debug["Access-Control-Allow-Headers"] = "*"
	if request.method == "POST":
		allProducts = json.loads(request.POST['data'])
		for currentRow in allProducts:
			product_type = ProductType.objects.get(text = currentRow['type'])
			if product_type:
				obj = Product.objects.get_or_create(
					type = product_type,
					description = currentRow["description"],
					fileURL = currentRow['filename'],
					idInType = 0
				)
		response = HttpResponse(len(json.loads(request.POST['data'])), mimetype = 'application/json')
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "*"
		return response
	return HttpResponse("Error, not a POST Request")

@csrf_exempt
def batchCreateAnswers(request):
	if request.method == 'POST':
#	        response = HttpResponse("Up in here, up in here", mimetype = 'application/json')
		allAnswers = json.loads(request.POST['data'])

		for currentRow in allAnswers:
			obj = Answer.objects.create(
                 		fromUser = User.objects.get(pk=currentRow['userID']), 
                       		forFacebookId = currentRow['friend'],
  	                	chosenProduct =  Product.objects.get(pk=currentRow['chosen']),
                        	wrongProduct =  Product.objects.get(pk=currentRow['wrong']),
                        	question = Question.objects.get(pk=currentRow['question'])
                	)
		response = HttpResponse(len(json.loads(request.POST['data'])), mimetype = 'application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"		
		return response
	return HttpResponse("Didn't work... Probably because this wasn't a POST request")

@csrf_exempt
#this is used for the training data, so it won't create feed objects or anything else
def createJustAnswers(request):
        if request.method == 'POST':
#               response = HttpResponse("Up in here, up in here", mimetype = 'application/json')
                allAnswers = json.loads(request.POST['data'])

                for currentRow in allAnswers:
                        obj = Answer.objects.create(
                                fromUser = User.objects.get(pk=currentRow['userID']),
                                forFacebookId = currentRow['friend'],
                                chosenProduct =  Product.objects.get(pk=currentRow['chosen']),
                                wrongProduct =  Product.objects.get(pk=currentRow['wrong']),
                                question = Question.objects.get(pk=currentRow['question'])
                        )
                response = HttpResponse(len(json.loads(request.POST['data'])), mimetype = 'application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
        return HttpResponse("Didn't work... Probably because this wasn't a POST request")


@csrf_exempt
def transferAnswers(request):
	now = datetime.datetime.now()
	earlier = now - datetime.timedelta(hours = 1)
	data = []
	recent_answers = Answer.objects.filter(created_at__range=(earlier,now))
	for answer in recent_answers:
		data.append({"forFacebookId": answer.forFacebookId, "fromUser": answer.fromUser.pk, "chosenProduct": answer.chosenProduct.id, "wrongProduct": answer.wrongProduct.id})
	# send a POST to ec2- with the answers
	url = "http://ec2-54-218-218-2.us-west-2.compute.amazonaws.com/data/uploadanswers"
	r = requests.post(url, data={"data": json.dumps(data)})
	
	response = HttpResponse(r.text)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
	return response

@csrf_exempt
def getListQuestionsForPersonalityType(request, user_id):
	types_to_rec = ["sports", "lottery", "careers"]
	products_list = []
	for p_type in types_to_rec:
		product_type = ProductType.objects.get(text=p_type)
		question = Question.objects.filter(type=product_type)[0]
		products = Product.objects.filter(type=product_type)
		p_combs = itertools.combinations(products, 2)
		for p_tuple in p_combs:
			if (Answer.objects.filter(forFacebookId = user_id).filter(Q(chosenProduct = p_tuple[0]) | Q(chosenProduct = p_tuple[1])).filter(Q(wrongProduct = p_tuple[0]) | Q(wrongProduct = p_tuple[1])).count()) > 0:
				continue	
			products_list.append({"question_text": question.text, "question_id": question.id, "product1": p_tuple[0].id, "product2": p_tuple[1].id, "product1_filename": p_tuple[0].fileURL, "product2_filename": p_tuple[1].fileURL})
	
	response = HttpResponse(json.dumps(products_list), mimetype = "application/json")
	response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"	
	return response


@csrf_exempt 
def updateUser (request, user_id):
	if request.method == 'POST':
		access_token = request.POST["access_token"]
        	current_user = User.objects.get(pk=user_id)
	
		names = []
		genders = []
		friends = []
		for friend_info in get_friends(access_token):
			friends.append(friend_info["uid"])
			names.append(friend_info["name"])
			genders.append(friend_info["sex"])
		current_user.names = names
		current_user.friends = friends
		current_user.genders = genders			
		top_friends = get_top_friends(access_token)
		
		top_friends.remove(int(user_id))
		current_user.topFriends = top_friends
		current_user.save()
		
		data = {"friends": friends, "genders": genders, "names": names, "top_friends": top_friends}

		response = HttpResponse(json.dumps(data), mimetype = 'application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
	return HttpResponse("Not a POST")

@csrf_exempt 
def createUser(request):
	if request.method == 'POST':
		access_token = request.POST["access_token"]
		profile = get_profile(access_token)
		facebook_id = profile["id"]
			
		obj, created = User.objects.get_or_create(facebookID=int(facebook_id))
		
		pic_url = "https://graph.facebook.com/" + facebook_id + "/picture?type=large&return_ssl_resources=1"
		user_profile = {
					"pictureURL": pic_url, 
					"name": profile["name"],
					"gender": profile["gender"],
					"birthday": profile["birthday"],
					"facebookId": profile["id"],
					"email": profile["email"]	
			}
		
		obj.profile = json.dumps(user_profile)
		obj.save()
		
		names = []
		genders = []
		friends = []
		for friend_info in get_friends(access_token):
			friends.append(friend_info["uid"])
			names.append(friend_info["name"])
			genders.append(friend_info["sex"])
					
		obj.friends =  friends
		obj.genders = genders
		obj.names = names
		
		top_friends = get_top_friends(access_token)
		try:
			top_friends.remove(facebook_id)
		except:
			pass	
		obj.topFriends = top_friends
		obj.save()

		data = {"friends": friends, "genders": genders, "names": names, "top_friends": top_friends}
		
		response = HttpResponse( json.dumps(data), mimetype = 'application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
	return HttpResponse()

@csrf_exempt
def newUser(request):
#	response = HttpResponse(serializers.serialize("json", request))
#	return response

	response = HttpResponse(str(request.POST))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
#	return response

	if request.method == 'POST':
		obj, created = User.objects.get_or_create(facebookID=int(request.POST['id_facebookID']))
#		obj = User.objects.create()		
		obj.facebookID = int(request.POST['id_facebookID'])
		#obj.socialIdentity =  request.POST['id_socialIdentity']
		obj.profile =  request.POST['id_profile']
		obj.friends =  request.POST['id_friends']
		obj.genders = request.POST['id_genders']
		obj.names = request.POST['id_names']
		try:
			if request.POST['id_mutual_friend_count']:
				obj.mutual_friend_count = request.POST['id_mutual_friend_count']
		except:
				obj.mutual_friend_count = []
		obj.save()

#		form = UserForm(request.POST)
#		user =  form.save()		
		
		response = HttpResponse("[{}]", mimetype = 'application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
	return HttpResponse()

def create(request):
	if request.method == 'POST':
		try:
			old = Data.objects.get(pk=request.POST['call'])
			form = DataForm(request.POST, instance = old)		
		except Data.DoesNotExist:
			form = DataForm(request.POST)		
		data = form.save()		
		print "\n\n" + serializers.serialize("json", [data]) + "\n\n"
		response = HttpResponse(serializers.serialize("json", [data]), mimetype='application/javascript')		
		response["Access-Control-Allow-Origin"] = "*"  
		response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
		response["Access-Control-Max-Age"] = "1000"  
		response["Access-Control-Allow-Headers"] = "*" 
		return response
