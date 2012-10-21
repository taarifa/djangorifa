import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_config.widgets import SelectDateWidget
from users.models import UserProfile

class UserEditProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_(u'First Name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last Name'), max_length=30)
    email = forms.EmailField(label=_(u'Email Address'), max_length=100)

    def __init__(self, *args, **kwargs):
        # Set to use crispy forms
        self.helper = FormHelper()
        being_created = kwargs.pop('being_created')
        if being_created:
            self.helper.form_tag = False

        else:
            self.helper.form_id = "id-users-create-form"
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Create'))

        # Initialise
        super(UserEditProfileForm, self).__init__(*args, **kwargs)

        # Add fields defined on user object
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except: pass

        # There should always be a user email
        self.fields['email'].initial = self.instance.user.email

        # Allow dob from 120 years ago - this may need changing when cryogenics takes off
        this_year = datetime.date.today().year
        years = range(this_year - 120, this_year)
        self.fields['dob'].widget = SelectDateWidget(years=years)

        # Put the user defined fields first key order
        ko = self.fields.keyOrder[-3:]
        ko.extend(self.fields.keyOrder[:-3])
        self.fields.keyOrder = ko

    def save(self, *args, **kwargs):
        super(UserEditProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        print self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()

    class Meta:
        model = UserProfile
        exclude = ('user',)

class UserRegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested mobile number is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    attrs_dict = {'class': 'required'}
    username = forms.RegexField(regex=r'^[\d]+$',
                                max_length=20,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Mobile Phone Number"),
                                error_messages={'invalid': _("This value may contain only numbers.")})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))

    def __init__(self, *args, **kwargs):
        # Set to use crispy forms
        self.helper = FormHelper()
        self.helper.form_id = "id-users-registration-form"
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

        # Initialise
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        # Add an email field
        self.cleaned_data['email'] = "%s@glassberg-powell.com" % self.cleaned_data['username']#"sms@messaging.clickatell.com" #"%s@taarifa.org" % self.cleaned_data['username']
        return self.cleaned_data
