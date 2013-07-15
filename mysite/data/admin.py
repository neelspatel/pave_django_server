from django.contrib import admin
from data.models import Question
from data.models import ProductType
from data.models import Product
from data.models import User
from data.models import Answer
from data.models import FeedObject
from data.models import Rec
from data.models import ProductTypeScoreAttributes
from data.models import ProductScore
from data.models import UserScore
from data.models import TrendingObject
from data.models import UserGeneratedQuestion, UserGeneratedProduct, UserGeneratedAnswer, QuestionQueue 
from data.models import QuestionObject 
from data.models import TrainingQuestion, TrainingAnswer, TrainingProduct, TrainingProductType

admin.site.register(User)

# TRAINING
admin.site.register(TrainingQuestion)
admin.site.register(TrainingAnswer)
admin.site.register(TrainingProduct)
admin.site.register(TrainingProductType)

# GAME PLAY
admin.site.register(QuestionObject)
admin.site.register(Question)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(FeedObject)
admin.site.register(Answer)

# USER GENERATED
admin.site.register(UserGeneratedQuestion)
admin.site.register(UserGeneratedProduct)
admin.site.register(UserGeneratedAnswer)
admin.site.register(QuestionQueue)

# TRENDING
admin.site.register(TrendingObject)
