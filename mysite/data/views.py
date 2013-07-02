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
	return HttpResponse("Hey, you're at the index for views in data")

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


@csrf_exempt
def getTrendingObjects(request, user_id):
	unique_types = TrendingObject.objects.values_list('type', flat=True).distinct()
	generated_objects = []
	for cur_type in unique_types:
		current_list = {}
		current_list[cur_type] = []
		cur_objects = TrendingObject.objects.filter(type = cur_type)
		for cur_object in cur_objects:
			cur_object.forUser = user_id
			cur_object.question_text = cur_object.question_text.replace("%n", "you")
			current_list[cur_type].append(model_to_dict(cur_object))

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
			objects_to_return.append({"question":current_object.questionText, "friend":friend, "chosenProduct":current_object.product1.fileURL, "otherProduct":current_object.product2.fileURL})
		for friend in current_object.fbFriend2:
                        objects_to_return.append({"question":current_object.questionText, "friend":friend, "chosenProduct":current_object.product2.fileURL, "otherProduct":current_object.product1.fileURL})
#	try:
# 		response = HttpResponse(serializers.serialize("json", FeedObject.objects.filter(forUser = user_id), fields=('id')), mimetype='application/json')
#	response = HttpResponse(serializers.serialize("json", objects_to_return))
	
	name = json.loads(User.objects.get(pk=user_id).profile)['name']

	for current_object in objects_to_return:
		current_object['question'] = current_object['question'].replace("%n", name.split()[0])


	response = HttpResponse(json.dumps(objects_to_return), mimetype = 'application/json')
#		response = HttpResponse(simplejson.dumps( [{"id": o.id} for o in FeedObject.objects.filter(forUser = user_id)]), mimetype='application/json')
#        except:
#	        response = HttpResponse(serializers.serialize("json", []), mimetype='application/json')

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
def newAnswer(request):
#       response = HttpResponse(serializers.serialize("json", request))
#       return response

        response = HttpResponse(str(request.POST))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        #return response

        if request.method == 'POST':
#                obj, created = User.objects.get_or_create(facebookID=request.POST['id_facebookID'])
#		obj = Answer()
                obj = Answer.objects.create(
			fromUser = User.objects.get(pk=request.POST['id_facebookID']),             
                	forFacebookId = request.POST['id_forFacebookID'],
                	#obj.socialIdentity =  request.POST['id_socialIdentity']
                	chosenProduct =  Product.objects.get(pk=request.POST['id_chosenProduct']),
			wrongProduct =  Product.objects.get(pk=request.POST['id_wrongProduct']),
			question = Question.objects.get(pk=request.POST['id_question']),
		)
#                obj.save()

#               form = UserForm(request.POST)
#               user =  form.save()             

                response = HttpResponse(str(request.POST), mimetype = 'application/json')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
        return HttpResponse()

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
				obj = Answer.objects.create(
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
def newUser(request):
#	response = HttpResponse(serializers.serialize("json", request))
#	return response

	response = HttpResponse(str(request.POST))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
	#return response

	if request.method == 'POST':
		obj, created = User.objects.get_or_create(facebookID=request.POST['id_facebookID'])
#		obj = User.objects.create()		
		obj.facebookID = request.POST['id_facebookID']
		#obj.socialIdentity =  request.POST['id_socialIdentity']
		obj.profile =  request.POST['id_profile']
		obj.friends =  request.POST['id_friends']
		obj.genders = request.POST['id_genders']
		obj.names = request.POST['id_names']
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
