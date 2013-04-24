# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TechnoFeature'
        db.create_table(u'stock_technofeature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('techno', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Techno'])),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Feature'])),
            ('int_value', self.gf('django.db.models.fields.IntegerField')()),
            ('str_value', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'stock', ['TechnoFeature'])

        # Adding model 'Techno'
        db.create_table(u'stock_techno', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Techno'], null=True)),
        ))
        db.send_create_signal(u'stock', ['Techno'])


    def backwards(self, orm):
        # Deleting model 'TechnoFeature'
        db.delete_table(u'stock_technofeature')

        # Deleting model 'Techno'
        db.delete_table(u'stock_techno')


    models = {
        u'game.feature': {
            'Meta': {'object_name': 'Feature'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'40'"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': "'40'"})
        },
        u'stock.asset': {
            'Meta': {'object_name': 'Asset'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assets'", 'to': u"orm['stock.Player']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assets'", 'to': u"orm['stock.System']"})
        },
        u'stock.planet': {
            'Meta': {'object_name': 'Planet'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'planets'", 'to': u"orm['stock.Asset']"}),
            'gravity': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ore': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'radiation': ('django.db.models.fields.IntegerField', [], {}),
            'revolt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'stability': ('django.db.models.fields.IntegerField', [], {}),
            'structure': ('django.db.models.fields.IntegerField', [], {}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'planets'", 'to': u"orm['stock.System']"}),
            'taxe': ('django.db.models.fields.IntegerField', [], {}),
            'terra': ('django.db.models.fields.IntegerField', [], {})
        },
        u'stock.player': {
            'Meta': {'object_name': 'Player'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'stock.system': {
            'Meta': {'object_name': 'System'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        },
        u'stock.techno': {
            'Meta': {'object_name': 'Techno'},
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['game.Feature']", 'through': u"orm['stock.TechnoFeature']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Techno']", 'null': 'True'})
        },
        u'stock.technofeature': {
            'Meta': {'object_name': 'TechnoFeature'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_value': ('django.db.models.fields.IntegerField', [], {}),
            'str_value': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'techno': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Techno']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['stock']