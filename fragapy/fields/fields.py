from django import forms
from django.contrib.humanize.templatetags.humanize import apnumber
from django.forms import CharField, ValidationError
from django.utils import simplejson
from django.template.defaultfilters import pluralize

from widgets import DictionaryInputs

class DictionaryField(CharField):
    """
    Utility field that doesn't convert returned value from widget to string.
    It keeps it as dictionary instead.    
    """
    widget = DictionaryInputs
    
    def clean(self, value):
        if not isinstance(value, dict):
            raise ValidationError(self.error_messages['invalid'])
        return value

class JSONField(CharField):
    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(JSONField, self).clean(value)
        try:
            json_data = simplejson.loads(value)
        except Exception, e:
            raise ValidationError(self.error_messages['invalid'])
        return json_data
        
class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple
    
    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', 0)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise ValidationError(self.error_messages['required'])
        if value and self.max_choices and len(value) > self.max_choices:
            raise ValidationError('You must select a maximum of %s choice%s.'
                    % (apnumber(self.max_choices), pluralize(self.max_choices)))
        return value
