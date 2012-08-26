from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.contenttypes.models import ContentType

from reports.models import Report, Reportable

class ReportForm(forms.ModelForm):

    """ Variables which should be overwritten by implementations """
    # The form action
    action = 'reports/new'

    # List of implementation classes of 'Reportable'
    reportables = [Reportable,]

    # The name of the implementation class of 'ReportedIssue'
    reported_issue = None

    # Dict of arguments to pass to the queryset. If none, defaults to all
    extra_reportable_args = None

    def __init__(self, *args, **kwargs):
        # Use crispy forms
        self.helper = FormHelper()
        self.helper.form_id = 'id-report-form'
        self.helper.form_method = 'post'
        self.helper.form_action = self.action
        self.helper.add_input(Submit('submit', 'Report'))
        super(ReportForm, self).__init__(*args, **kwargs)

        # Indicates whether there are any reportables
        self.has_reportables = False

        # Generate the checkboxes
        for r in self.i_reportables():
            self.has_reportables = True
            self.generate_checkboxes(r)

    # Provides an iteration for looping through the reportables
    def i_reportables(self):
        for reportable in self.reportables:
            if reportable._meta.abstract:
                for r in reportable.__subclasses__():
                    yield r
            else:
                yield reportable

    # Creates one group of checkboxes
    def generate_checkboxes(self, reportable):
        if self.extra_reportable_args:
            qs = reportable.objects.filter(**self.extra_reportable_args)
        else:
            qs = reportable.objects.all()

        if qs.count() > 0:
            self.fields[reportable.__name__] = forms.ModelMultipleChoiceField(
                queryset=qs,
                widget=forms.CheckboxSelectMultiple(),
                required=False,
            )

    """
        Default clean method for report
        Ensures at least one issue is checked
    """
    def clean(self, *args, **kwargs):
        super(ReportForm, self).clean(*args, **kwargs)
        is_checked = False

        for r in self.i_reportables():
            # If the field doesn't exist, move on
            data = self.cleaned_data.get(r.__name__)
            if not data: continue

            # At least one checkbox is checked
            is_checked = True

            # Perform any other validation required by subform
            self.clean_reportable(r, data)

        if not is_checked:
            raise forms.ValidationError('At least one issue must be reported.')

        return self.cleaned_data
        """

        for reportable in self.reportable:
            if reportable._meta.abstract:
                for r in reportable.__subclasses"""

    """
        Default save method for a report
        Args:
            request (obj): The request object
        Return:
            report (Report): The report created
    """
    def save(self, request, *args, **kwargs):
        # Need to add the user back into the report
        self.instance.user = request.user

        # Save the report
        report = super(ReportForm, self).save(*args, **kwargs)

        # For all the generated checkboxes, add to report
        for r in self.i_reportables():
            self.save_issue(report, r)

        # Save the report - mutable object so will save
        report.save()
        return report

    def save_issue(self, report, reportable):
        # Check if the reportable is on the form
        boxes = self.cleaned_data.get(reportable.__name__)
        if not boxes: return

        for box in boxes:
            content_type = ContentType.objects.get_for_model(box)
            # Get additional arguments for the issue
            extra = self.get_extra_create_args(box)

            # If not already existing, create
            # Status must be below 4
            (reported_issue, _) = self.reported_issue.objects.get_or_create(
                # Generic contenttype bug in Django
                # NEED to do it this way
                content_type = content_type,
                object_id = box.pk,
                status__lte=3,
                **extra)

            # Add the issue to the report
            report.issues.connect(reported_issue)

    """
        Must provide additional arguments to create the issue
        override this method and return them

        Args:
            reportable (obj): An instance of an object subclassing reportable

        Return:
            args (dict): A dictionary of arguments to pass to 'get_or_create'
    """
    def get_extra_create_args(self, reportable):
      raise NotImplementedError, "This method must be implemented or reports creation will fail."

    """
        Any additional clean to be performed per checkbox
        Args:
            reportable_class (obj): The class of the reportable being cleaned
            reportable_instances (list): The list of instances checked on the form
    """
    def clean_reportable(self, reportable_class, reportable_instances):
        pass

    class Meta:
        model = Report
        # Exclude non-editable fields
        exclude = ('user','status')
