# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductType'
        db.create_table(u'data_producttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'data', ['ProductType'])

        # Adding model 'Question'
        db.create_table(u'data_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ProductType'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'data', ['Question'])

        # Adding model 'Product'
        db.create_table(u'data_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ProductType'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('fileURL', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('idInType', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'data', ['Product'])

        # Adding model 'User'
        db.create_table(u'data_user', (
            ('facebookID', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True)),
            ('socialIdentity', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('profile', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('friends', self.gf('data.models.ListField')()),
            ('names', self.gf('data.models.ListField')()),
            ('genders', self.gf('data.models.ListField')()),
            ('friendsInApp', self.gf('data.models.ListField')(blank=True)),
        ))
        db.send_create_signal(u'data', ['User'])

        # Adding model 'FeedObject'
        db.create_table(u'data_feedobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forUser', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('product1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product1', to=orm['data.Product'])),
            ('image1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('fbFriend1', self.gf('data.models.ListField')()),
            ('product1Count', self.gf('django.db.models.fields.IntegerField')()),
            ('product2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product2', to=orm['data.Product'])),
            ('image2', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('fbFriend2', self.gf('data.models.ListField')(blank=True)),
            ('product2Count', self.gf('django.db.models.fields.IntegerField')()),
            ('currentQuestion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='currentQuestion', to=orm['data.Question'])),
            ('questionText', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('updatedAt', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'data', ['FeedObject'])

        # Adding model 'Answer'
        db.create_table(u'data_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fromUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.User'])),
            ('forFacebookId', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('chosenProduct', self.gf('django.db.models.fields.related.ForeignKey')(related_name='chosenProduct', to=orm['data.Product'])),
            ('wrongProduct', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wrongProduct', to=orm['data.Product'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='question', to=orm['data.Question'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'data', ['Answer'])

        # Adding model 'Rec'
        db.create_table(u'data_rec', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.User'])),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ProductType'])),
            ('attribute_score_1', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_2', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_3', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_4', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_5', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_6', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_7', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_8', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_9', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_10', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'data', ['Rec'])

        # Adding model 'ProductTypeScoreAttributes'
        db.create_table(u'data_producttypescoreattributes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ProductType'])),
            ('attribute_score_1', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('attribute_score_2', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('attribute_score_3', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('attribute_score_4', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('attribute_score_5', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('attribute_score_6', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('attribute_score_7', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('attribute_score_8', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('attribute_score_9', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('attribute_score_10', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'data', ['ProductTypeScoreAttributes'])

        # Adding model 'Insight'
        db.create_table(u'data_insight', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rec_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ProductType'])),
        ))
        db.send_create_signal(u'data', ['Insight'])

        # Adding model 'ProductScore'
        db.create_table(u'data_productscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Product'])),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ProductType'])),
            ('attribute_score_1', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_2', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_3', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_4', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_5', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_6', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_7', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_8', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_9', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_10', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'data', ['ProductScore'])

        # Adding model 'UserScore'
        db.create_table(u'data_userscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.User'])),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ProductType'])),
            ('attribute_score_1', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_2', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_3', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_4', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_5', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_6', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_7', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_8', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_9', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attribute_score_10', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'data', ['UserScore'])

        # Adding model 'TrendingObject'
        db.create_table(u'data_trendingobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product1_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product1_id', to=orm['data.Product'])),
            ('product2_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product2_id', to=orm['data.Product'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Question'])),
            ('question_text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('product1_count', self.gf('django.db.models.fields.IntegerField')()),
            ('product2_count', self.gf('django.db.models.fields.IntegerField')()),
            ('image1', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('image2', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('forUser', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'data', ['TrendingObject'])


    def backwards(self, orm):
        # Deleting model 'ProductType'
        db.delete_table(u'data_producttype')

        # Deleting model 'Question'
        db.delete_table(u'data_question')

        # Deleting model 'Product'
        db.delete_table(u'data_product')

        # Deleting model 'User'
        db.delete_table(u'data_user')

        # Deleting model 'FeedObject'
        db.delete_table(u'data_feedobject')

        # Deleting model 'Answer'
        db.delete_table(u'data_answer')

        # Deleting model 'Rec'
        db.delete_table(u'data_rec')

        # Deleting model 'ProductTypeScoreAttributes'
        db.delete_table(u'data_producttypescoreattributes')

        # Deleting model 'Insight'
        db.delete_table(u'data_insight')

        # Deleting model 'ProductScore'
        db.delete_table(u'data_productscore')

        # Deleting model 'UserScore'
        db.delete_table(u'data_userscore')

        # Deleting model 'TrendingObject'
        db.delete_table(u'data_trendingobject')


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
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProductType']"})
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