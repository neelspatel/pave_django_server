# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from recs.models import Answer
from recs.models import Rec

import simplejson
@csrf_exempt
def index():
	return HTTPResponse("Hello World")

def new(request):
	if request.method == 'POST':
		try:
			# get the answer from the POST variables 
			answer = request.POST['answer']
			productTypeVal = answer["type"]
			userId = anser["answerForFacebookId"]
			# see if a rec has been logged for the same user_id and product_type
			currentRec = Rec.objects.filter(productType = productTypeVal).filter(userId = userIdVal)
		except:
			print "Broke"
			# was not able to find the Rec in the database
		
	# update the Rec object with the winningProductId score
	return HTTPResponse ("Called the new function")

	
