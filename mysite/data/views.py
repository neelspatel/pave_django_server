# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from data.models import Data
from data.models import DataForm
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import simplejson
from django.core import serializers


@csrf_exempt
def index(request):
	return HttpResponse("Hey, you're at the index for views in data")

@csrf_exempt
def detail(request, data_id):
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
