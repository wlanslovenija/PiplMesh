import datetime

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import mongoengine

GENDER_CHOICES = (
    ('male', _('Male')),
    ('female', _('Female'))
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

        # TODO: This is not needed right?
        if self.upper_limit and not isinstance(self.upper_limit, datetime.datetime):
            self.error(u'Invalid limit.')
        if self.lower_limit and not isinstance(self.lower_limit, datetime.datetime):
            self.error(u'Invalid limit.')

        super(LimitedDateTimeField, self).__init__(*args, **kwargs)
   
    def validate(self, value):
        super(LimitedDateTimeField, self).validate(value)
        
        if isinstance(value, datetime.datetime)
            value = value.date()
        if self.upper_limit and value > self.upper_limit.date():
            self.error(u'Value is out of bounds.')
        if self.lower_limit and value < self.lower_limit.date():
            self.error(u'Value is out of bounds.')