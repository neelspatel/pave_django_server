from django.db import models
from django.forms import ModelForm
import os
from django.conf import settings
from django.db.models import Q
import ast
import datetime
import calendar
from south.modelsinspector import add_introspection_rules
import simplejson as json
#from rec_views import updateRecVector

add_introspection_rules([], ["^data\.models\.ListField"])

#defining a list field
class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_db_prep_value(self, value, connection=None, prepared=None):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class User(models.Model):
        facebookID = models.CharField(max_length=200, primary_key=True)
        socialIdentity = models.TextField(blank=True)
        profile = models.TextField(blank=True)
	topFriends = ListField(blank=True, null=True)
        friends = ListField()
        male_friends = ListField(null=True)
	female_friends = ListField(null=True)
	names = ListField()
        genders = ListField()
	mutual_friend_count = ListField(blank=True)
        friendsInApp = ListField(blank=True)
	level = models.IntegerField(default=1)

        def save(self, *args, **kwargs):
                self.friendsInApp = list ( set(self.friends).intersection(set( [int(x) for x in [ o.pk for o in User.objects.all()]] )))
                super(User, self).save(*args, **kwargs)
		notif = Notification.objects.get_or_create(user=self)

        def __unicode__(self):
                try:
			name = str(json.loads(self.profile)["name"])
		except:
			name = self.facebookID
		return name


class Notification(models.Model):
	user = models.ForeignKey(User, unique = True)
	number_answers = models.IntegerField(default=0)
	number_ug_answers = models.IntegerField(default=0)
	number_recs = models.IntegerField(default=0)
	status_score = models.IntegerField(default=0)		
	answers_since_update = models.IntegerField(default=0)
	last_rec_update = models.DateTimeField(null=True)
	rec_ready = models.BooleanField(default=False)
	#scale = models.FloatField(default = 1.0)
	def __unicode__(self):
		return str(self.user) + ": " + str(self.status_score)

class ToRecommend(models.Model):
	url = models.CharField(max_length=200)
	text = models.CharField(max_length=200)
	def __unciode__(self):
		return self.url

class Recommendation(models.Model):
	user = models.ForeignKey(User, db_index = True)
	rec = models.ForeignKey(ToRecommend, db_index = True)
	delivered = models.BooleanField(default=False)	
	agree = models.NullBooleanField(null=True)

# Create your models here
class ProductType(models.Model):
	text = models.CharField(max_length=200, unique = True)
	count = models.IntegerField()
        def __unicode__(self):
                return self.text

class Question(models.Model):
	type = models.ForeignKey(ProductType)
	text = models.TextField()
	on = models.BooleanField(default=True)
	def __unicode__(self):
		return self.text
	
class Product(models.Model):
        type = models.ForeignKey(ProductType)
	on = models.BooleanField(default=True)
        description = models.TextField()
        fileURL = models.CharField(max_length=200, db_index = True)
        idInType = models.IntegerField()

        def save(self, *args, **kwargs):
                self.idInType = self.type.count
                self.type.count = self.type.count + 1
                self.type.save()
		super(Product, self).save(*args, **kwargs)
       
	def __unicode__(self):
                return (str(self.type) + ": " + self.description + " at " + self.fileURL)

class UserForm(ModelForm):
        class Meta:
                model = User

class QuestionObject(models.Model):
	# need to change FBFriend1 to a comma seperated value for product 1, FBFriend2 list of people who voted for product 2
	toUser = models.ForeignKey(User, related_name = "qo_to_user", db_index = True)
	aboutFriend = models.CharField(max_length=200)
	aboutFriendName = models.CharField(max_length = 200)
	product1 = models.ForeignKey(Product, related_name = 'qo_product1')
	image1 = models.CharField(max_length=200)
	product2 = models.ForeignKey(Product, related_name = 'qo_product2')
	image2 = models.CharField(max_length=200)
	product1Count = models.IntegerField()
	product2Count = models.IntegerField()
	currentQuestion = models.ForeignKey(Question, related_name = 'qo_currentQuestion')
	questionText = models.CharField(max_length=200)
	createdAt = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return (str(self.toUser) + ": " + str(self.image1) + ", " + str(self.image2) + ": " + str(self.questionText))


class FeedObject(models.Model):
	# need to change FBFriend1 to a comma seperated value for product 1, FBFriend2 list of people who voted for product 2
	forUser = models.CharField(max_length=200, db_index = True)
#	forUser = models.ForeignKey(User, related_name = 'forUser')
	product1 = models.ForeignKey(Product, related_name = 'fo_product1')
	image1 = models.CharField(max_length=200)
	fbFriend1 = ListField(null=True)
#	fbFriend1 = models.ForeignKey(User, related_name = 'fbFriend1')
	product1Count = models.IntegerField()
	product2 = models.ForeignKey(Product, related_name = 'fo_product2')
	image2 = models.CharField(max_length=200)
	fbFriend2 = ListField(null=True)
#	fbFriend2 = models.ForeignKey(User, related_name = 'fbFriend2', null = True, blank = True)
	product2Count = models.IntegerField()
	currentQuestion = models.ForeignKey(Question, related_name = 'fo_currentQuestion')
	questionText = models.CharField(max_length=200)
	updatedAt = models.IntegerField()

	def save(self, *args, **kwargs):
		self.updatedAt = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
		super(FeedObject, self).save(*args, **kwargs)
		
	def __unicode__(self):
		return (str(self.forUser) + ": " + str(self.image1) + " (" + str(self.product1Count) + ") " + str(self.image2) + " (" + str(self.product2Count) + ") for " + str(self.questionText))

class Answer(models.Model):
	fromUser = models.ForeignKey(User, db_index=True)
	forFacebookId = models.CharField(max_length=200, db_index = True)
	chosenProduct = models.ForeignKey(Product, related_name = 'chosenProduct')
	wrongProduct = models.ForeignKey(Product, related_name = 'wrongProduct')
	question = models.ForeignKey(Question, related_name = 'question')
	anonymousUser = models.ForeignKey(User, blank=True, null=True, related_name = 'a_user')
	created_at = models.DateTimeField(auto_now_add = True)

	def save(self, *args, **kwargs):
		#first check if it is about themselves; if so, we don't need to change any feed object
		if(int(self.fromUser.pk) == int(self.forFacebookId)):
			super(Answer, self).save(*args, **kwargs)
		else:
			results = FeedObject.objects.filter(Q(product1 = self.chosenProduct) | Q(product1 = self.wrongProduct))
			results = results.filter(Q(product2 = self.chosenProduct) | Q(product2 = self.wrongProduct))
			results = results.filter(forUser = self.forFacebookId)
			results = results.filter(currentQuestion = self.question)

			#first check if there are any results
	#		friendList = [1]
			if results.count() == 0:
				newFeedObject = FeedObject(product1=self.chosenProduct, image1=self.chosenProduct.fileURL, fbFriend1=[int(self.fromUser.pk)], product1Count = 1,  product2=self.wrongProduct, image2=self.wrongProduct.fileURL, fbFriend2=[], product2Count = 0, currentQuestion=self.question, questionText = self.question.text, forUser= self.forFacebookId)    
				newFeedObject.save()
			else:
				newFeedObject = results[0]
				#determines ordering of the products
				if self.chosenProduct == newFeedObject.product1:
					newFeedObject.fbFriend1.append(int(self.fromUser.pk))
					newFeedObject.product1Count = newFeedObject.product1Count + 1
				
				else:
					newFeedObject.fbFriend2.append(int(self.fromUser.pk))
                               		newFeedObject.product2Count = newFeedObject.product2Count + 1

				newFeedObject.save()
			super(Answer, self).save(*args, **kwargs)

	def __unicode__(self):
		return (self.fromUser.facebookID + " answered " + self.question.text  + " for " + self.forFacebookId + " chose " + str(self.chosenProduct.fileURL) + " over " + str(self.wrongProduct.fileURL))

############# USER GENERATED MODELS #################################################################
class UserGeneratedProduct(models.Model):
        on = models.BooleanField(default=True)
        fileURL = models.CharField(max_length=200, db_index = True)
        user = models.ForeignKey(User)
        description = models.CharField(max_length=200, null=True)
	def __unicode__(self):
                return self.fileURL


class UserGeneratedQuestion(models.Model):
	user = models.ForeignKey(User, db_index = True)
	text = models.TextField()
	on = models.BooleanField(default=True)
	fbFriend1 = ListField(blank=True)
	fbFriend2 = ListField(blank=True)
	product1 = models.ForeignKey(UserGeneratedProduct, related_name = "product_1")		
	product2 = models.ForeignKey(UserGeneratedProduct, related_name = "product_2")
	product1_count = models.IntegerField(default=0)
	product2_count = models.IntegerField(default=0)
	def __unicode__(self):
		return self.text


class QuestionQueue(models.Model):
	toUser = models.ForeignKey(User, related_name = "to_user", db_index = True)
	byUser = models.ForeignKey(User, related_name = "by_user")
	question = models.ForeignKey(UserGeneratedQuestion)
	on = models.BooleanField(default = True)
	created_at = models.DateTimeField(auto_now_add = True)	

class UserGeneratedAnswer(models.Model):
	fromUser = models.ForeignKey(User, related_name = "from_user")
	forUser = models.ForeignKey(User, related_name = "for_user", db_index = True)
	chosenUGProduct = models.ForeignKey(UserGeneratedProduct, related_name = "chosen_user_gen_products")
	wrongUGProduct = models.ForeignKey(UserGeneratedProduct, related_name = "wrong_user_gen_product")
	question = models.ForeignKey(UserGeneratedQuestion)
	created_at = models.DateTimeField(auto_now_add = True)
	
	def save(self, *args, **kwargs):
		q = self.question
		if (q.product1 == self.chosenUGProduct):
			q.fbFriend1.append(self.fromUser.pk)
			q.product1_count += 1
		else:	
			q.fbFriend2.append(self.fromUser.pk)
			q.product2_count += 1
		q.save()
		super(UserGeneratedAnswer, self).save(*args, **kwargs)
		

			
############# TRAINING MODELS ###############################################################################

class TrainingProductType(models.Model):
	text = models.CharField(max_length=200, unique = True)
	def __unicode__(self):
		return str(self.text)

class TrainingProduct(models.Model):
	on = models.BooleanField(default=True)
	type = models.ForeignKey(TrainingProductType)
	fileURL = models.CharField(max_length=200, db_index=True)
	description= models.TextField(null=True)
	def __unicode__(self):
		return str(self.fileURL)
	
class TrainingQuestion(models.Model):
	type = models.ForeignKey(TrainingProductType)
	text = models.TextField()
	on = models.BooleanField(default=True)
	def __unicode__(self):
		return str(self.text)

class TrainingAnswer(models.Model):
	user = models.ForeignKey(User, db_index=True)
	wrongProduct = models.ForeignKey(TrainingProduct, related_name="t_wrong_product")
	chosenProduct = models.ForeignKey(TrainingProduct, related_name="t_chosen_product")
	question = models.ForeignKey(TrainingQuestion, related_name="t_question")
	created_at = models.DateTimeField(auto_now_add = True)
		
	def save(self, *args, **kwargs):	
		super (TrainingAnswer, self).save(*args, **kwargs)

#############################################################################################################
class Rec (models.Model):
	user_id = models.ForeignKey(User)
	product_type = models.ForeignKey(ProductType)
	attribute_score_1 = models.IntegerField(null = True)
        attribute_score_2 = models.IntegerField(null = True)
        attribute_score_3 = models.IntegerField(null = True)
        attribute_score_4 = models.IntegerField(null = True)
        attribute_score_5 = models.IntegerField(null = True)
        attribute_score_6 = models.IntegerField(null = True)
        attribute_score_7 = models.IntegerField(null = True)
        attribute_score_8 = models.IntegerField(null = True)
        attribute_score_9 = models.IntegerField(null = True)
        attribute_score_10 = models.IntegerField(null = True)
	count = models.IntegerField(null = True)

class ProductTypeScoreAttributes(models.Model):
	product_type_id = models.ForeignKey(ProductType)
	attribute_score_1 = models.CharField(max_length = 200, null = True)
        attribute_score_2 = models.CharField(max_length = 200, null = True)
        attribute_score_3 = models.CharField(max_length = 200, null = True)
        attribute_score_4 = models.CharField(max_length = 200, null = True)
        attribute_score_5 = models.CharField(max_length = 200, null = True)
        attribute_score_6 = models.CharField(max_length = 200, null = True)
        attribute_score_7 = models.CharField(max_length = 200, null = True)
        attribute_score_8 = models.CharField(max_length = 200, null = True)
        attribute_score_9 = models.CharField(max_length = 200, null = True)
        attribute_score_10 = models.CharField(max_length = 200, null = True)


class Insight (models.Model):
	# update
	rec_id = models.ForeignKey(ProductType)

class ProductScore (models.Model):
	product_id = models.ForeignKey(Product)
	product_type = models.ForeignKey(ProductType)
	attribute_score_1 = models.IntegerField(null = True)
	attribute_score_2 = models.IntegerField(null = True)
	attribute_score_3 = models.IntegerField(null = True)
	attribute_score_4 = models.IntegerField(null = True)
	attribute_score_5 = models.IntegerField(null = True)
	attribute_score_6 = models.IntegerField(null = True)
	attribute_score_7 = models.IntegerField(null = True)
	attribute_score_8 = models.IntegerField(null = True)
	attribute_score_9 = models.IntegerField(null = True)
	attribute_score_10 = models.IntegerField(null = True)

class UserScore (models.Model):
	user_id = models.ForeignKey(User)
	product_type = models.ForeignKey(ProductType)
	attribute_score_1 = models.IntegerField(null = True)
        attribute_score_2 = models.IntegerField(null = True)
        attribute_score_3 = models.IntegerField(null = True)
        attribute_score_4 = models.IntegerField(null = True)
        attribute_score_5 = models.IntegerField(null = True)
        attribute_score_6 = models.IntegerField(null = True)
        attribute_score_7 = models.IntegerField(null = True)
        attribute_score_8 = models.IntegerField(null = True)
        attribute_score_9 = models.IntegerField(null = True)
        attribute_score_10 = models.IntegerField(null = True)

class TrendingObject (models.Model):
	product1_id = models.ForeignKey(Product, related_name = 'product1_id')
	product2_id = models.ForeignKey(Product, related_name = 'product2_id')
	question = models.ForeignKey(Question)
	question_text = models.CharField(max_length = 200)
	product1_count = models.IntegerField()
	product2_count = models.IntegerField()
	image1 = models.CharField(max_length=200, blank=True)
	image2 = models.CharField(max_length=200, blank=True)
	type = models.CharField(db_index=True, max_length = 200)
	forUser = models.CharField(null=True, blank=True, max_length=200)
	
	def increment(self, product_id, from_user_id, for_user_id):
		if product_id == product1_id:
			self.product1_count += 1
			 #create an answer
	                answer = Answer.create(fromUser = from_user_id, forFacebookId = for_user_id, chosenProduct = self.product1_id, wrongProduct = self.product2_id, question = self.question)
		else:
			self.product2_count += 1
			 #create an answer
	                answer = Answer.create(fromUser = from_user_id, forFacebookId = for_user_id, chosenProduct = self.product2_id, wrongProduct = self.product1_id, question = self.question)

		self.save()

		#create an answer
		answer = Answer.create(fromUser = from_user_id, forFacebookId = for_user_id, chosenProduct = self.product1_id, wrongProduct = self.product2_id, question = self.question)

	def save(self, *args, **kwargs):
                self.image1 = self.product1_id.fileURL
		self.image2 = self.product2_id.fileURL
                super(TrendingObject, self).save(*args, **kwargs)
