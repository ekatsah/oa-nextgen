# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FleetFeature'
        db.create_table(u'stock_fleetfeature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Feature'])),
            ('int_value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('str_value', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('fleet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Fleet'])),
        ))
        db.send_create_signal(u'stock', ['FleetFeature'])

        # Adding model 'FleetCargo'
        db.create_table(u'stock_fleetcargo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Feature'])),
            ('int_value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('str_value', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('fleet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Fleet'])),
        ))
        db.send_create_signal(u'stock', ['FleetCargo'])

        # Adding model 'SchemeFeature'
        db.create_table(u'stock_schemefeature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Feature'])),
            ('int_value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('str_value', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Scheme'])),
        ))
        db.send_create_signal(u'stock', ['SchemeFeature'])

        # Adding model 'SchemeMerch'
        db.create_table(u'stock_schememerch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Feature'])),
            ('int_value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('str_value', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Scheme'])),
        ))
        db.send_create_signal(u'stock', ['SchemeMerch'])

        # Adding model 'Scheme'
        db.create_table(u'stock_scheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schemes', to=orm['stock.Player'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schemes_in_domain', to=orm['game.Feature'])),
        ))
        db.send_create_signal(u'stock', ['Scheme'])

        # Adding model 'Fleet'
        db.create_table(u'stock_fleet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fleets', to=orm['stock.Player'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('pos_x', self.gf('django.db.models.fields.IntegerField')()),
            ('pos_y', self.gf('django.db.models.fields.IntegerField')()),
            ('dest_x', self.gf('django.db.models.fields.IntegerField')()),
            ('dest_y', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'stock', ['Fleet'])

        # Adding model 'FleetCompo'
        db.create_table(u'stock_fleetcompo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fleet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Fleet'])),
            ('scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Scheme'])),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Feature'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('dammage', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'stock', ['FleetCompo'])

        # Adding model 'SchemeCompo'
        db.create_table(u'stock_schemecompo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Scheme'])),
            ('techno', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Techno'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'stock', ['SchemeCompo'])


    def backwards(self, orm):
        # Deleting model 'FleetFeature'
        db.delete_table(u'stock_fleetfeature')

        # Deleting model 'FleetCargo'
        db.delete_table(u'stock_fleetcargo')

        # Deleting model 'SchemeFeature'
        db.delete_table(u'stock_schemefeature')

        # Deleting model 'SchemeMerch'
        db.delete_table(u'stock_schememerch')

        # Deleting model 'Scheme'
        db.delete_table(u'stock_scheme')

        # Deleting model 'Fleet'
        db.delete_table(u'stock_fleet')

        # Deleting model 'FleetCompo'
        db.delete_table(u'stock_fleetcompo')

        # Deleting model 'SchemeCompo'
        db.delete_table(u'stock_schemecompo')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assets'", 'to': u"orm['stock.Player']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assets'", 'to': u"orm['stock.System']"})
        },
        u'stock.fleet': {
            'Meta': {'object_name': 'Fleet'},
            'cargos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'in_fleets'", 'symmetrical': 'False', 'through': u"orm['stock.FleetCargo']", 'to': u"orm['game.Feature']"}),
            'compos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stock.Scheme']", 'through': u"orm['stock.FleetCompo']", 'symmetrical': 'False'}),
            'dest_x': ('django.db.models.fields.IntegerField', [], {}),
            'dest_y': ('django.db.models.fields.IntegerField', [], {}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['game.Feature']", 'through': u"orm['stock.FleetFeature']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fleets'", 'to': u"orm['stock.Player']"}),
            'pos_x': ('django.db.models.fields.IntegerField', [], {}),
            'pos_y': ('django.db.models.fields.IntegerField', [], {})
        },
        u'stock.fleetcargo': {
            'Meta': {'object_name': 'FleetCargo'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Feature']"}),
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Fleet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_value': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'str_value': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'stock.fleetcompo': {
            'Meta': {'object_name': 'FleetCompo'},
            'dammage': ('django.db.models.fields.IntegerField', [], {}),
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Fleet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Feature']"}),
            'scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Scheme']"})
        },
        u'stock.fleetfeature': {
            'Meta': {'object_name': 'FleetFeature'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Feature']"}),
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Fleet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_value': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'str_value': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
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
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'technos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'owner'", 'symmetrical': 'False', 'to': u"orm['stock.Techno']"})
        },
        u'stock.scheme': {
            'Meta': {'object_name': 'Scheme'},
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'compos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stock.Techno']", 'through': u"orm['stock.SchemeCompo']", 'symmetrical': 'False'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schemes_in_domain'", 'to': u"orm['game.Feature']"}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['game.Feature']", 'through': u"orm['stock.SchemeFeature']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merch': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'schemes_contains'", 'symmetrical': 'False', 'through': u"orm['stock.SchemeMerch']", 'to': u"orm['game.Feature']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schemes'", 'to': u"orm['stock.Player']"})
        },
        u'stock.schemecompo': {
            'Meta': {'object_name': 'SchemeCompo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Scheme']"}),
            'techno': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Techno']"})
        },
        u'stock.schemefeature': {
            'Meta': {'object_name': 'SchemeFeature'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_value': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Scheme']"}),
            'str_value': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'stock.schememerch': {
            'Meta': {'object_name': 'SchemeMerch'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_value': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Scheme']"}),
            'str_value': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'stock.system': {
            'Meta': {'object_name': 'System'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        },
        u'stock.techno': {
            'Meta': {'object_name': 'Techno'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Techno']", 'null': 'True'}),
            'raw_features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['game.Feature']", 'through': u"orm['stock.TechnoFeature']", 'symmetrical': 'False'})
        },
        u'stock.technofeature': {
            'Meta': {'object_name': 'TechnoFeature'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_value': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'str_value': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'techno': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Techno']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['stock']