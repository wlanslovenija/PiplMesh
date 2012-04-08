import datetime

from django import forms

from piplmesh.account import models

class LimitedDateTimeField(forms.DateTimeField):
    def __init__(self, upper_limit=None, lower_limit=None, input_formats=None, *args, **kwargs):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        if self.upper_limit and not isinstance(self.upper_limit, (datetime.datetime, datetime.date)):
            raise ValidationError(models.error_messages['syntax_upper'])
        if self.lower_limit and not isinstance(self.lower_limit, (datetime.datetime, datetime.date)):
            raise ValidationError(models.error_messages['syntax_lower'])

        super(FormLimitedDateTimeField, self).__init__(input_formats=None, *args, **kwargs)
   

    def clean(self, value):
        value = super(LimitedDateTimeField, self).clean(value)

        def error():
            raise ValidationError(models.error_messages['bounds'])

        models.limit_date(value, self.lower_limit, self.upper_limit, error)

        return value