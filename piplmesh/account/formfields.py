import datetime

from django import forms

from piplmesh.account import fields

class LimitedDateTimeField(forms.DateTimeField):
    def __init__(self, upper_limit=None, lower_limit=None, input_formats=None, *args, **kwargs):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        if self.upper_limit and not isinstance(self.upper_limit, (datetime.datetime, datetime.date)):
            raise forms.ValidationError(fields.error_messages['syntax_upper'])
        if self.lower_limit and not isinstance(self.lower_limit, (datetime.datetime, datetime.date)):
            raise forms.ValidationError(fields.error_messages['syntax_lower'])

        super(LimitedDateTimeField, self).__init__(input_formats=None, *args, **kwargs)
   

    def clean(self, value):
        value = super(LimitedDateTimeField, self).clean(value)

        def error():
            raise forms.ValidationError(fields.error_messages['bounds'])

        fields.limit_date(value, self.lower_limit, self.upper_limit, error)

        return value