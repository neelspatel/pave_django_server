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

admin.site.register(Question)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(FeedObject)
admin.site.register(Answer)
admin.site.register(ProductTypeScoreAttributes)
admin.site.register(ProductScore)
admin.site.register(UserScore)
admin.site.register(Rec)
admin.site.register(TrendingObject)
