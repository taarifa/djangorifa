from django.forms.extras.widgets import SelectDateWidget as SDW

class SelectDateWidget(SDW):
    def create_select(self, name, field, value, val, choices):
        self.none_value = (0, field.strip("%s_").title())
        return super(SelectDateWidget, self).create_select(name, field, value, val, choices)
