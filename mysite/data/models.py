from django.db import models
from django.forms import ModelForm

# Create your models here.
class Data(models.Model):

	value = models.TextField()

	def __unicode__(self):
		return self.value
