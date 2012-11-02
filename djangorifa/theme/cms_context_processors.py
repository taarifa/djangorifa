from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

def crispy_forms(instance, placeholder):
    if type(instance).__name__ == "CMSFormDefinition":
        helper = FormHelper()
        helper.add_input(Submit('submit', 'Submit'))
        return {'crispy_forms_helper': helper}
    return {}
