# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FacilityCategory'
        db.create_table('facilities_facilitycategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('vital', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('facilities', ['FacilityCategory'])

        # Adding model 'Facility'
        db.create_table('facilities_facility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['facilities.FacilityCategory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(unique=True)),
        ))
        db.send_create_signal('facilities', ['Facility'])

        # Adding model 'FacilityIssue'
        db.create_table('facilities_facilityissue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, max_length=1)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['facilities.Facility'])),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('facilities', ['FacilityIssue'])

        # Adding model 'Part'
        db.create_table('facilities_part', (
            ('reportable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reports.Reportable'], unique=True, primary_key=True)),
            ('min_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('max_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
        ))
        db.send_create_signal('facilities', ['Part'])

        # Adding M2M table for field category on 'Part'
        db.create_table('facilities_part_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('part', models.ForeignKey(orm['facilities.part'], null=False)),
            ('facilitycategory', models.ForeignKey(orm['facilities.facilitycategory'], null=False))
        ))
        db.create_unique('facilities_part_category', ['part_id', 'facilitycategory_id'])

        # Adding model 'Maintenance'
        db.create_table('facilities_maintenance', (
            ('reportable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reports.Reportable'], unique=True, primary_key=True)),
            ('min_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('max_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
        ))
        db.send_create_signal('facilities', ['Maintenance'])

        # Adding M2M table for field category on 'Maintenance'
        db.create_table('facilities_maintenance_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('maintenance', models.ForeignKey(orm['facilities.maintenance'], null=False)),
            ('facilitycategory', models.ForeignKey(orm['facilities.facilitycategory'], null=False))
        ))
        db.create_unique('facilities_maintenance_category', ['maintenance_id', 'facilitycategory_id'])


    def backwards(self, orm):
        # Deleting model 'FacilityCategory'
        db.delete_table('facilities_facilitycategory')

        # Deleting model 'Facility'
        db.delete_table('facilities_facility')

        # Deleting model 'FacilityIssue'
        db.delete_table('facilities_facilityissue')

        # Deleting model 'Part'
        db.delete_table('facilities_part')

        # Removing M2M table for field category on 'Part'
        db.delete_table('facilities_part_category')

        # Deleting model 'Maintenance'
        db.delete_table('facilities_maintenance')

        # Removing M2M table for field category on 'Maintenance'
        db.delete_table('facilities_maintenance_category')


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