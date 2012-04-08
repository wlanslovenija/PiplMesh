import datetime

from django.conf import settings

import mongoengine

from piplmesh.account import models

def get_initial_language(request=None):
    return settings.LANGUAGE_CODE

class LanguageField(mongoengine.StringField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 5)
        kwargs.setdefault('choices', settings.LANGUAGES)
        kwargs.setdefault('default', get_initial_language)
        
        super(LanguageField, self).__init__(*args, **kwargs)

class GenderField(mongoengine.StringField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 6)
        kwargs.setdefault('choices', models.GENDER_CHOICES)
        kwargs.setdefault('default', models.GENDER_CHOICES[1][0])
        
        super(GenderField, self).__init__(*args, **kwargs)

class LimitedDateTimeField(mongoengine.DateTimeField):
    def __init__(self, upper_limit=None, lower_limit=None, *args, **kwargs):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        if self.upper_limit and not isinstance(self.upper_limit, (datetime.datetime, datetime.date)):
            self.error(models.error_messages['syntax_upper'])
        if self.lower_limit and not isinstance(self.lower_limit, (datetime.datetime, datetime.date)):
            self.error(models.error_messages['syntax_lower'])

        super(LimitedDateTimeField, self).__init__(*args, **kwargs)
   
    def validate(self, value):
        super(LimitedDateTimeField, self).validate(value)

        def error():
            raise self.error(models.error_messages['bounds'])
        
        models.limit_date(value, self.lower_limit, self.upper_limit, error)