from django.db import models

# Create your models here.

class Rec(models.Model):
	productType = models.CharField(max_length=200)
	userFacebookId = models.CharField(max_length = 100)
	pub_date = models.DateTimeField('date-published')

class Answer(models.Model):
	answerForFacebookId = models.CharField(max_length = 50);
	answerFromUserId = models.CharField(max_length = 100);
	losingProductId = models.CharField(max_length = 100);
	winningProductid = models.CharField(max_length = 100);
	questionId = models.CharField(max_length = 100);
	questionText = models.CharField(max_length = 200);
	pub_date = models.DateTimeField('date-published');

class Product(models.Model):
	productId = models.CharField(max_length = 100);
	score = models.CharField(max_length = 100) 

class Insight(models.Model):
	product_type = models.CharField(max_length=200)
	# figure out how to represent Insight



