from django.core.management.base import BaseCommand, CommandError
from data.models import FeedObjects, Products, ProductTypes, Questions

class Command(BaseCommnad):

	args = '<>'
	help = 'Finds the top trending questions and saves them to WoldWide'
	
	def handle(self, *args, **options):
		# need to loop through all of the 
