import datetime

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import mongoengine

GENDER_CHOICES = (
    ('male', _('male')),
    ('female', _('female'))
)

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
        kwargs.setdefault('choices', GENDER_CHOICES)
        kwargs.setdefault('default', GENDER_CHOICES[1][0])
        
        super(GenderField, self).__init__(*args, **kwargs)

class LimitedDateTimeField(mongoengine.DateTimeField):
    def __init__(self, upper_limit=None, lower_limit=None, *args, **kwargs):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        if self.upper_limit and not isinstance(self.upper_limit, (datetime.datetime, datetime.date)):
            self.error(u'Invalid upper_limit argument.')
        if self.lower_limit and not isinstance(self.lower_limit, (datetime.datetime, datetime.date)):
            self.error(u'Invalid lower_limit argument.')

        super(LimitedDateTimeField, self).__init__(*args, **kwargs)
   
    def validate(self, value):
        super(LimitedDateTimeField, self).validate(value)
        
        if self.upper_limit:
            tmp_value = value
            tmp_upper_limit = self.upper_limit
            if not isinstance(value, datetime.datetime) or not isinstance(self.upper_limit, datetime.datetime):
                if isinstance(self.upper_limit, datetime.datetime):
                    tmp_upper_limit = self.upper_limit.date()
                elif isinstance(tmp_value, datetime.datetime):
                    tmp_value = value.date()
            if tmp_value > tmp_upper_limit:
                self.error(u'Value is out of bounds.')
                    
        if self.lower_limit:
            tmp_value = value
            tmp_lower_limit = self.lower_limit
            if not isinstance(value, datetime.datetime) or not isinstance(self.lower_limit, datetime.datetime):
                if isinstance(self.lower_limit, datetime.datetime):
                    tmp_lower_limit = self.lower_limit.date()
                elif isinstance(tmp_value, datetime.datetime):
                    tmp_value = value.date()
            if tmp_value < tmp_lower_limit:
                self.error(u'Value is out of bounds.')