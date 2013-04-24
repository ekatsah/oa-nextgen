# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'System'
        db.create_table(u'stock_system', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')()),
            ('y', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'stock', ['System'])

        # Adding model 'Player'
        db.create_table(u'stock_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40, db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'stock', ['Player'])

        # Adding model 'Asset'
        db.create_table(u'stock_asset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assets', to=orm['stock.System'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='50')),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assets', to=orm['stock.Player'])),
        ))
        db.send_create_signal(u'stock', ['Asset'])

        # Adding model 'Planet'
        db.create_table(u'stock_planet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='planets', to=orm['stock.System'])),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='planets', to=orm['stock.Asset'])),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('gravity', self.gf('django.db.models.fields.IntegerField')()),
            ('radiation', self.gf('django.db.models.fields.IntegerField')()),
            ('structure', self.gf('django.db.models.fields.IntegerField')()),
            ('terra', self.gf('django.db.models.fields.IntegerField')()),
            ('taxe', self.gf('django.db.models.fields.IntegerField')()),
            ('stability', self.gf('django.db.models.fields.IntegerField')()),
            ('ore', self.gf('django.db.models.fields.IntegerField')()),
            ('revolt', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'stock', ['Planet'])


    def backwards(self, orm):
        # Deleting model 'System'
        db.delete_table(u'stock_system')

        # Deleting model 'Player'
        db.delete_table(u'stock_player')

        # Deleting model 'Asset'
        db.delete_table(u'stock_asset')

        # Deleting model 'Planet'
        db.delete_table(u'stock_planet')


    models = {
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
        }
    }

    complete_apps = ['stock']