from django.contrib.gis.db import models
from django.contrib.gis.db.models import GeoManager
from reports.models import Reportable, ReportedIssue
from genericm2m.models import RelatedObjectsDescriptor

class FacilityCategory(models.Model):
    name = models.CharField(max_length=255)
    # If vital, it's dealt with quicker than for a non-vital facility
    vital = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Facility(models.Model):
    category = models.ForeignKey(FacilityCategory)
    name = models.CharField(max_length=255, help_text='If the facility has a specific name', blank=True, null=True)
    description = models.TextField(blank=True)
    location = models.PointField(unique=True)

    # Important - it deals with the location stuff
    objects = GeoManager()

    def __unicode__(self):
        string = "Facility %d, %s" % (self.pk, self.category)
        if self.name:
            string += ": %s" % self.name
        return string

    class Meta:
        app_label = 'facilities'
        verbose_name_plural = 'facilities'

class FacilityIssue(ReportedIssue):
    # Holds a foreign key link to the facility in question
    facility = models.ForeignKey(Facility)
    # Enables auction to override cost
    cost = models.DecimalField(max_digits=9, decimal_places=2, help_text='The initial cost of the issue')
    # To prevent concurrent editing, needs a locked field
    locked = models.BooleanField()

    related = RelatedObjectsDescriptor()

class FacilityReportable(Reportable):
    category = models.ManyToManyField(FacilityCategory)
    min_cost = models.DecimalField(max_digits=9, decimal_places=2, help_text="Minimum cost to fix")
    max_cost = models.DecimalField(max_digits=9, decimal_places=2, help_text="Maximum cost to fix")

    class Meta:
        abstract = True

# Place all reportable things here - make sure to subclass FacilityReportable
class Part(FacilityReportable):
    pass

class Maintenance(FacilityReportable):
    pass
