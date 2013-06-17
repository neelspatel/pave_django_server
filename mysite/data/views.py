# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import simplejson
from django.core import serializers
from data.models import Question
from data.models import Product
from data.models import User
from data.models import UserForm
from data.models import FeedObject
from data.models import Answer
from random import randint
import logging
import urllib

@csrf_exempt
def index(request):
	return HttpResponse("Hey, you're at the index for views in data")

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
def getAllFeedObjects(request, user_id):
        ids = []
	try:
# 		response = HttpResponse(serializers.serialize("json", FeedObject.objects.filter(forUser = user_id), fields=('id')), mimetype='application/json')
		response = HttpResponse(simplejson.dumps( [{"id": o.id} for o in FeedObject.objects.filter(forUser = user_id)]), mimetype='application/json')
        except:
	        response = HttpResponse(serializers.serialize("json", []), mimetype='application/json')

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
		obj.save()

#		form = UserForm(request.POST)
#		user =  form.save()		
		
		response = HttpResponse(str(request.POST), mimetype = 'application/json')
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
