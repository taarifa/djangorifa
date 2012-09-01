from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

class AuctionFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Set to use crispy forms
        self.helper = FormHelper()
        self.helper.form_id = 'id-auction-filter-form'
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Filter'))
        self.helper.form_class = "horizontal"

        # Initialise
        super(AuctionFilterForm, self).__init__(*args, **kwargs)