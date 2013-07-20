from django.core.management.base import BaseCommand, CommandError
from data.models import User, QuestionObject, Question, FeedObject, Product, ProductType
from collections import Counter
import random

class Command(BaseCommand):

	args = '<>'
	help = 'Finds the top trending questions and saves them to WoldWide'
	
	def getFriendWithValidName(self, current_user, gender = None):
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

	def random_combinations(self, iterable, length, num):
		pool = tuple(iterable)
		result = []
		for i in range(num):
			indices = sorted(random.sample(xrange(length), 2))
			result.append(list(pool[i] for i in indices))
		return result

	def updateQuestionObjectQueue(self, current_user, count=100, replace=False):
		# maybe very slow
		q_list = Question.objects.filter(on = True).order_by("?")[:count]
		# get unique product types
		p_types_counter = Counter([question.type for question in q_list])
		p_types_products = {}
		for p_type, count in p_types_counter.iteritems():
			 # get a list of pairs of two random products of the given product time
			curr_len = Product.objects.filter(type=p_type).filter(on=True).count()
			curr_products = Product.objects.filter(type=p_type).filter(on=True)
			p_types_products[p_type] = self.random_combinations(curr_products, curr_len, (count * 2))
					
		if p_types_products:
			# delete all of the questions for this user
			if replace:
				QuestionObject.objects.filter(toUser=current_user).delete()
				
			# we got a non-empty dictionary
			qq_list = []
			for question in q_list:
				# add a new object to the QuestionObject for the current user
				# package for the client			
				# deal with male female
				if question.text.endswith("_male"):
					current_friend = self.getFriendWithValidName(current_user, "male")
				elif question.text.endswith("female"):
					 current_friend = self.getFriendWithValidName(current_user, "fenale")
				else:
					current_friend = self.getFriendWithValidName(current_user)
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


	def handle(self, *args, **options):
		self.stdout.write("In handle")		
		MIN_QUESTIONS = 500

		# algorithm for getting random questions
		
		# need to loop through all of the 
		users = User.objects.all()

		# force evaluation of query set
		for user in users:
			qo_queue_count = QuestionObject.objects.filter(toUser = user).count()
			if qo_queue_count < MIN_QUESTIONS:
				self.updateQuestionObjectQueue(user, MIN_QUESTIONS)
				

