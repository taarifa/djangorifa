# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TaarifaConfig.bounding_points'
        db.delete_column('taarifa_config_taarifaconfig', 'bounding_points')

        # Adding field 'TaarifaConfig.bounds'
        db.add_column('taarifa_config_taarifaconfig', 'bounds',
                      self.gf('django.contrib.gis.db.models.fields.PolygonField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'TaarifaConfig.bounding_points'
        db.add_column('taarifa_config_taarifaconfig', 'bounding_points',
                      self.gf('django.contrib.gis.db.models.fields.PolygonField')(default=0),
                      keep_default=False)

        # Deleting field 'TaarifaConfig.bounds'
        db.delete_column('taarifa_config_taarifaconfig', 'bounds')


    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taarifa_config.taarifaconfig': {
            'Meta': {'object_name': 'TaarifaConfig'},
            'bounds': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'})
        }
    }

    complete_apps = ['taarifa_config']