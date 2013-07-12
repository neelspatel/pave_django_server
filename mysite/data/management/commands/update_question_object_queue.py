from django.core.management.base import BaseCommand, CommandError
from data.models import User, QuestionObject, Question, FeedObject, Product, ProductType

class Command(BaseCommand):

	args = '<>'
	help = 'Finds the top trending questions and saves them to WoldWide'
	
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
				
			# we got a non-empty dictionary
			qq_list = []
			for question in q_list:
				# add a new object to the QuestionObject for the current user
				# package for the client			
				# deal with male female
				if question.text.endswith("_male"):
					current_friend = getFriendWithValidName(current_user, "male")
				elif question.text.endswith("female"):
					 current_friend = getFriendWithValidName(current_user, "fenale")
				else:
					current_friend = getFriendWithValidName(current_user)
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
		
		MIN_QUESTIONS = 500

		# algorithm for getting random questions
		
		# need to loop through all of the 
		users = User.objects.all()

		# force evaluation of query set
		for user in users:
			qo_queue_count = QuestionObject.objects.filter(toUser = user).count()
			if qo_queue_count < MIN_QUESTIONS:
				updateQuestionObjectQueue(user, MIN_QUESTIONS)
				

