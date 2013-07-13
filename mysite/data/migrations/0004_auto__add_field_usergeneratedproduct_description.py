# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserGeneratedProduct.description'
        db.add_column(u'data_usergeneratedproduct', 'description',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserGeneratedProduct.description'
        db.delete_column(u'data_usergeneratedproduct', 'description')


    models = {
        u'data.answer': {
            'Meta': {'object_name': 'Answer'},
            'chosenProduct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'chosenProduct'", 'to': u"orm['data.Product']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forFacebookId': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'fromUser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question'", 'to': u"orm['data.Question']"}),
            'wrongProduct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wrongProduct'", 'to': u"orm['data.Product']"})
        },
        u'data.feedobject': {
            'Meta': {'object_name': 'FeedObject'},
            'currentQuestion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'currentQuestion'", 'to': u"orm['data.Question']"}),
            'fbFriend1': ('data.models.ListField', [], {}),
            'fbFriend2': ('data.models.ListField', [], {'blank': 'True'}),
            'forUser': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'image2': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'product1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product1'", 'to': u"orm['data.Product']"}),
            'product1Count': ('django.db.models.fields.IntegerField', [], {}),
            'product2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product2'", 'to': u"orm['data.Product']"}),
            'product2Count': ('django.db.models.fields.IntegerField', [], {}),
            'questionText': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updatedAt': ('django.db.models.fields.IntegerField', [], {})
        },
        u'data.insight': {
            'Meta': {'object_name': 'Insight'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rec_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProductType']"})
        },
        u'data.product': {
            'Meta': {'object_name': 'Product'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'fileURL': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idInType': ('django.db.models.fields.IntegerField', [], {}),
            'on': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProductType']"})
        },
        u'data.productscore': {
            'Meta': {'object_name': 'ProductScore'},
            'attribute_score_1': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_10': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_2': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_3': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_4': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_5': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_6': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_7': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_8': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_9': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Product']"}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProductType']"})
        },
        u'data.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'data.producttypescoreattributes': {
            'Meta': {'object_name': 'ProductTypeScoreAttributes'},
            'attribute_score_1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'attribute_score_10': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'attribute_score_2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'attribute_score_3': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'attribute_score_4': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'attribute_score_5': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'attribute_score_6': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'attribute_score_7': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'attribute_score_8': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'attribute_score_9': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_type_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProductType']"})
        },
        u'data.question': {
            'Meta': {'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProductType']"})
        },
        u'data.questionqueue': {
            'Meta': {'object_name': 'QuestionQueue'},
            'byUser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'by_user'", 'to': u"orm['data.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.UserGeneratedQuestion']"}),
            'toUser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': u"orm['data.User']"})
        },
        u'data.rec': {
            'Meta': {'object_name': 'Rec'},
            'attribute_score_1': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_10': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_2': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_3': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_4': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_5': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_6': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_7': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_8': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_9': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProductType']"}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.User']"})
        },
        u'data.trendingobject': {
            'Meta': {'object_name': 'TrendingObject'},
            'forUser': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'image2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'product1_count': ('django.db.models.fields.IntegerField', [], {}),
            'product1_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product1_id'", 'to': u"orm['data.Product']"}),
            'product2_count': ('django.db.models.fields.IntegerField', [], {}),
            'product2_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product2_id'", 'to': u"orm['data.Product']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Question']"}),
            'question_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        },
        u'data.user': {
            'Meta': {'object_name': 'User'},
            'facebookID': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'friends': ('data.models.ListField', [], {}),
            'friendsInApp': ('data.models.ListField', [], {'blank': 'True'}),
            'genders': ('data.models.ListField', [], {}),
            'names': ('data.models.ListField', [], {}),
            'profile': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'socialIdentity': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'data.usergeneratedanswer': {
            'Meta': {'object_name': 'UserGeneratedAnswer'},
            'chosenUGProduct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'chosen_user_gen_products'", 'to': u"orm['data.UserGeneratedProduct']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forUser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'for_user'", 'to': u"orm['data.User']"}),
            'fromUser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_user'", 'to': u"orm['data.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.UserGeneratedQuestion']"}),
            'wrongUGProduct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wrong_user_gen_product'", 'to': u"orm['data.UserGeneratedProduct']"})
        },
        u'data.usergeneratedproduct': {
            'Meta': {'object_name': 'UserGeneratedProduct'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'fileURL': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.User']"})
        },
        u'data.usergeneratedquestion': {
            'Meta': {'object_name': 'UserGeneratedQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_1'", 'to': u"orm['data.UserGeneratedProduct']"}),
            'product1_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'product2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_2'", 'to': u"orm['data.UserGeneratedProduct']"}),
            'product2_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.User']"})
        },
        u'data.userscore': {
            'Meta': {'object_name': 'UserScore'},
            'attribute_score_1': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_10': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_2': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_3': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_4': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_5': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_6': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_7': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_8': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attribute_score_9': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProductType']"}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.User']"})
        }
    }

    complete_apps = ['data']