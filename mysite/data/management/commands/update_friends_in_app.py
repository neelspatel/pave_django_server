from django.core.management.base import BaseCommand, CommandError
from data.models import User

class Command(BaseCommand):

	args = '<>'
	help = 'Finds the top trending questions and saves them to WoldWide'
	
	def handle(self, *args, **options):
		
		# need to loop through all of the 
		users = User.objects.all()

		# force evaluation of query set
		user_list = list(users)
		user_id_list = [user.facebookID for user in user_list]
		for user in user_list:
			friends = user.friends 
			current_friend_in_app = []
			for friend in friends:
				if str(friend) in user_id_list:
					 current_friends_in_app.append(friend)
			# make sure that it is unique
			current_friends_in_app = list(set(current_friends_in_app))
			user.friendsInApp = current_friends_in_app
			user.save()

