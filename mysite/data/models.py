from django.db import models
from django.forms import ModelForm
import os
from django.conf import settings
from django.db.models import Q
import ast

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

# Create your models here
class ProductType(models.Model):
	text = models.CharField(max_length=200)
	count = models.IntegerField()
        def __unicode__(self):
                return self.text

class Question(models.Model):
	type = models.ForeignKey(ProductType)
	text = models.TextField()

	def __unicode__(self):
		return self.text

class Product(models.Model):
        type = models.ForeignKey(ProductType)
        description = models.TextField()
        fileURL = models.CharField(max_length=200)
        idInType = models.IntegerField()

        def save(self, *args, **kwargs):
                self.idInType = self.type.count
                self.type.count = self.type.count + 1
                self.type.save()
       
	def __unicode__(self):
                return (str(self.type) + ": " + self.description + " at " + self.fileURL)

class User(models.Model):
        facebookID = models.CharField(max_length=200, primary_key=True)
        socialIdentity = models.TextField(blank=True)
        profile = models.TextField(blank=True)
        friends = ListField()
	names = ListField()
	genders = ListField()
	friendsInApp = ListField(blank=True)
#	friends = models.CommaSeparatedIntegerField()

	def save(self, *args, **kwargs):
		self.friendsInApp = list ( set(self.friends).intersection(set( [int(x) for x in [ o.pk for o in User.objects.all()]] )))
		super(User, self).save(*args, **kwargs)

	def __unicode__(self):
		return str(self.facebookID)

class UserForm(ModelForm):
        class Meta:
                model = User

class FeedObject(models.Model):
	# need to change FBFriend1 to a comma seperated value for product 1, FBFriend2 list of people who voted for product 2
	forUser = models.CharField(max_length=200)
#	forUser = models.ForeignKey(User, related_name = 'forUser')
	product1 = models.ForeignKey(Product, related_name = 'product1')
	image1 = models.CharField(max_length=200)
	fbFriend1 = ListField()
#	fbFriend1 = models.ForeignKey(User, related_name = 'fbFriend1')
	product1Count = models.IntegerField()
	product2 = models.ForeignKey(Product, related_name = 'product2')
	image2 = models.CharField(max_length=200)
	fbFriend2 = ListField(blank=True)
#	fbFriend2 = models.ForeignKey(User, related_name = 'fbFriend2', null = True, blank = True)
	product2Count = models.IntegerField()
	currentQuestion = models.ForeignKey(Question, related_name = 'currentQuestion')
	questionText = models.CharField(max_length=200)
		
	def __unicode__(self):
		return (str(self.forUser) + ": " + str(self.image1) + " (" + str(self.product1Count) + ") " + str(self.image2) + " (" + str(self.product2Count) + ") for " + str(self.questionText))

class Answer(models.Model):
	fromUser = models.ForeignKey(User)
	forFacebookId = models.CharField(max_length=200)
	chosenProduct = models.ForeignKey(Product, related_name = 'chosenProduct')
	wrongProduct = models.ForeignKey(Product, related_name = 'wrongProduct')
	question = models.ForeignKey(Question, related_name = 'question')

	def save(self, *args, **kwargs):
		#first check if it is about themselves; if so, we don't need to change any feed object
		if(int(self.fromUser.pk) == int(self.forFacebookId)):
			trending_object = TrendingObject.objects.filter(Q(product1_id = self.chosenProduct) | Q(product1_id = self.wrongProduct))
			trending_object = trending_object.filter(Q(product2_id = self.chosenProduct) | Q(product2_id = self.wrongProduct))
			trending_object = trending_object.filter(question = self.question)
			final_object = trending_object[0]
			
			#now figure out which count to update
			if(final_object.product1_id == self.chosenProduct):
				final_object.product1_count += 1
			else:
				final_object.product2_count += 1

			#now save the answer
			final_object.save() 
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

			new_results = ProductScore.objects.filter(product_id = self.chosenProduct)
			if new_results.count() != 0:
				# product does have a score
				# get the product score
				product_score = new_results[0]
				rec_result = Rec.objects.filter(Q(user_id = User.objects.get(pk =self.forFacebookId)) | Q(product_type = self.question.type))
				if rec_result.count() == 0:
					# save and upadatea new Rec for the given user becuase it does not exist
					newRec = Rec(user_id = User.objects.get(pk=self.forFacebookId), product_type = self.question.type, attribute_score_1 = product_score.attribute_score_1,

							attribute_score_2 = product_score.attribute_score_2,
							attribute_score_3 = product_score.attribute_score_3,
							attribute_score_4 = product_score.attribute_score_4,
                        	                        attribute_score_5 = product_score.attribute_score_5,
                                	                attribute_score_6 = product_score.attribute_score_6,
                                        	        attribute_score_7 = product_score.attribute_score_7,
                                               		attribute_score_8 = product_score.attribute_score_8,
                                      		        attribute_score_9 = product_score.attribute_score_9,
                                               		attribute_score_10 = product_score.attribute_score_10,
							count = 1
						)
					newRec.save()
				else:
					# update the rec
					current_rec = rec_result[0]
					current_rec.count += 1
					current_rec.attribute_score_1 += product_score.attribute_score_1
					current_rec.attribute_score_2 += product_score.attribute_score_2					
                                	current_rec.attribute_score_3 += product_score.attribute_score_3
                                	current_rec.attribute_score_4 += product_score.attribute_score_4
                                	current_rec.attribute_score_5 += product_score.attribute_score_5
                                	current_rec.attribute_score_6 += product_score.attribute_score_6
                                	current_rec.attribute_score_7 += product_score.attribute_score_7
                                	current_rec.attribute_score_8 += product_score.attribute_score_8
                                	current_rec.attribute_score_9 += product_score.attribute_score_9
                                	current_rec.attribute_score_10 += product_score.attribute_score_10
					current_rec.save()			
			super(Answer, self).save(*args, **kwargs)

	def __unicode__(self):
		return (self.fromUser.facebookID + " answered " + self.question.text  + " for " + self.forFacebookId + " chose " + str(self.chosenProduct.fileURL) + " over " + str(self.wrongProduct.fileURL))

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
	
	def save(self, *args, **kwargs):
                self.image1 = self.product1_id.fileURL
		self.image2 = self.product2_id.fileURL
                super(TrendingObject, self).save(*args, **kwargs)
