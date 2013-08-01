from django.core.management.base import BaseCommand, CommandError
from data.models import Answer
import requests
import datetime
import json

class Command(BaseCommand):

	args = '<>'
	help = "sends over all answers that were created within the last hour to the processing database" 
	
	def handle(self, *args, **options):	
		url = "http://ec2-54-218-218-2.us-west-2.compute.amazonaws.com/data/uploadanswers"
		now_time = datetime.datetime.now()
		earlier = now_time - datetime.timedelta(minutes = 1)
		data = []
		recent_answers = Answer.objects.filter(created_at__range=(earlier,now_time))
		self.stdout.write(str(len(recent_answers)))
		if (not recent_answers):
			self.stdout.write("not recent answers")
			return
		else:
			for answer in recent_answers:
				data.append({"forFacebookId": answer.forFacebookId, "fromUser": answer.fromUser.pk, "chosenProduct": answer.chosenProduct.id, "wrongProduct": answer.wrongProduct.id})
			# send a POST to ec2- with the answers
			r = requests.post(url, data={"data": json.dumps(data)})
			self.stdout.write(r.text)		
	



