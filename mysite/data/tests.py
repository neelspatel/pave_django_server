"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from data.models import Product, ProductType, Question, Answer, User
from django.test.client import Client
import factory

class UserFactory(factory.Factory):
	FACTORY_FOR = User
	facebookID = factory.Sequence(lambda n: '%s' %n)
	socialIdentity = ''
	profile = ''
	friends = ['123']
	genders = ['male']
	names = ['Side Tester']
	friendsInApp = ['123']

class ProductTypeFactory(factory.Factory):
	FACTORY_FOR = ProductType
	text = factory.Iterator(["male_shoe", "shirts", "movies"])
	count = 3
	
class ProductFactory(factory.Factory):
	FACTORY_FOR = Product
	type = factory.SubFactory(ProductTypeFactory)
	on = True
	description = 'cool shoes'
	fileURL = 'image-' 
	idInType = 0		

class QuestionFactory(factory.Factory):
	FACTORY_FOR = Question
	type = factory.SubFactory(ProductTypeFactory)
	text  = factory.Iterator(["Which one do you like better", "Cooler?" "More?"])
	on = True
	
class AnswerFactory(factory.Factory):
	FACTORY_FOR = Answer
	forFacebookId = "1"
	chosenProduct = factory.SubFactory(ProductFactory)
	wrongProduct = factory.SubFactory(ProductFactory)
	question = factory.SubFactory(QuestionFactory)
		

# things that we want to test:
# ensure that endpoints are behaving properly
# ensure that user can create an answer
# ensure that the endpoints return a non-empty dictionary
# get list of questions returns something of 100 objects long
class GetListQuestionsTest(TestCase):
	def setUp(self):
	#	self.type = ProductType.objects.create(text = "male_shoes", count = 0)
	#	self.product1 = Product.objects.create(type = self.type, on = True, description = "yessir", fileURL = "image1.jpg")
	#A	self.product2 = Product.objects.create(type = self.type, on = True, description = "yessir", fileURL = "image2.jpg")
#		self.user = User.objects.create(facebookID='551733910', profile = '', socialIdentity = '', friends = ['123'], names = ["Side"], genders = ["male"], friendsInApp = [])
	#	self.question = Question.objects.create(type = self.type, text = "Which one", on=True)
	#	self.answer = Answer.objects.create(forFacebookId = '1', chosenProduct = self.product1, wrongProduct = self.product2, fromUser = self.user, question= self.question)
		self.client = Client()
		self.user = UserFactory()
		self.product=ProductFactory()
		self.question=QuestionFactory()
		self.answer=AnswerFactory()
				 
	def test_get_questions(self):
		url = '/data/getlistquestionsnew/' + self.user.facebookID + '/'
		response = self.client.get(url)
		self.assertEqual(200, response.status_code)
		self.assertContains(response, self.question.text)
#define the things that need to work in the server side
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
