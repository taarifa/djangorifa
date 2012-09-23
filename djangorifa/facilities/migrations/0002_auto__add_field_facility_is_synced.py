# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Facility.is_synced'
        db.add_column('facilities_facility', 'is_synced',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Facility.is_synced'
        db.delete_column('facilities_facility', 'is_synced')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'facilities.facility': {
            'Meta': {'object_name': 'Facility'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facilities.FacilityCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_synced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'facilities.facilitycategory': {
            'Meta': {'object_name': 'FacilityCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vital': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'facilities.facilityissue': {
            'Meta': {'object_name': 'FacilityIssue'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facilities.Facility']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'max_length': '1'})
        },
        'facilities.maintenance': {
            'Meta': {'object_name': 'Maintenance'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['facilities.FacilityCategory']", 'symmetrical': 'False'}),
            'max_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'min_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'reportable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reports.Reportable']", 'unique': 'True', 'primary_key': 'True'})
        },
        'facilities.part': {
            'Meta': {'object_name': 'Part'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['facilities.FacilityCategory']", 'symmetrical': 'False'}),
            'max_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'min_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'reportable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reports.Reportable']", 'unique': 'True', 'primary_key': 'True'})
        },
        'reports.reportable': {
            'Meta': {'object_name': 'Reportable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['facilities']