# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feature'
        db.create_table(u'game_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length='40')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='40')),
            ('type', self.gf('django.db.models.fields.CharField')(max_length='40')),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'game', ['Feature'])


    def backwards(self, orm):
        # Deleting model 'Feature'
        db.delete_table(u'game_feature')


    models = {
        u'game.feature': {
            'Meta': {'object_name': 'Feature'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'40'"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': "'40'"})
        }
    }

    complete_apps = ['game']