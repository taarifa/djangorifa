from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from reports.helpers import STATUS_CHOICES
from reports.tasks import send_status_mail, update_reports_status
from genericm2m.models import RelatedObjectsDescriptor

# This class holds all fields common to what can be reported
# For example, this will be subclassed by "facility part" or "facility maintenance"
class Reportable(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # Whether or not to show the reportable in the report form
    show = models.BooleanField()

    # Returns what the reportable is, and the name of the reportable
    def __unicode__(self):
        return self.name

# This class holds all the reported problems and their current status.
# This is automatically generated, and will not be editable by an admin.
# This class is abstract, and needs to be implemented in the proper
# application with the foreign key it's an issue for
class ReportedIssue(models.Model):
    created = models.DateField(auto_now_add=True)
    # Each reported issue needs a status. These are defined in the helpers class.
    status = models.PositiveIntegerField(max_length=1, choices=STATUS_CHOICES, default=1)

    # Holds a generic link to a reportable object
    content_type = models.ForeignKey(ContentType, verbose_name="Type of Job")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    #reportable = models.ForeignKey(Reportable)

    related = RelatedObjectsDescriptor()

    def __unicode__(self):
        return "%s: %s" % (self.content_object.__class__.__name__, self.content_object)

    # Override the save method to perform tasks on status change
    def save(self, *args, **kwargs):
        # Only applicable when editing the model
        if self.pk:
            old_instance = type(self).objects.get(pk=self.pk)
            if not old_instance.status == self.status:
                update_reports_status.delay(self)
                send_status_mail.delay(self)
        super(ReportedIssue, self).save(*args, **kwargs)

    class Meta:
        abstract = True


# This class is a way to consolidate the issues that each user has reported.
class Report(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    user = models.ForeignKey(User)
    description = models.CharField(max_length=255)
    status = models.DecimalField(max_digits=5, default=0, decimal_places=2)

    # The report needs to hold all the issues, and each issue may be in a different report.
    # For this reason, we need a generic many-to-many field
    #issues = models.ManyToManyField(ReportedIssue)
    issues = RelatedObjectsDescriptor()

    def __unicode__(self):
        return "Report %d" % self.pk
