import datetime

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import mongoengine

GENDER_CHOICES = (
    ('male', _('male')),
    ('female', _('female'))
)

error_messages = {
    'bounds': _(u"Value is out of bounds."),
    'syntax_lower': _(u"Invalid lower_limit argument."),
    'syntax_upper': _(u"Invalid upper_limit argument."),
}

def limit_date(value, lower_limit, upper_limit, error):
    if upper_limit:
        tmp_value = value
        tmp_upper_limit = upper_limit
        if not isinstance(value, datetime.datetime) or not isinstance(upper_limit, datetime.datetime):
            if isinstance(upper_limit, datetime.datetime):
                tmp_upper_limit = upper_limit.date()
            elif isinstance(tmp_value, datetime.datetime):
                tmp_value = value.date()
        if tmp_value > tmp_upper_limit:
            error()
                
    if lower_limit:
        tmp_value = value
        tmp_lower_limit = lower_limit
        if not isinstance(value, datetime.datetime) or not isinstance(lower_limit, datetime.datetime):
            if isinstance(lower_limit, datetime.datetime):
                tmp_lower_limit = lower_limit.date()
            elif isinstance(tmp_value, datetime.datetime):
                tmp_value = value.date()
        if tmp_value < tmp_lower_limit:
            error()

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
            self.error(error_messages['syntax_upper'])
        if self.lower_limit and not isinstance(self.lower_limit, (datetime.datetime, datetime.date)):
            self.error(error_messages['syntax_lower'])

        super(LimitedDateTimeField, self).__init__(*args, **kwargs)
   
    def validate(self, value):
        super(LimitedDateTimeField, self).validate(value)

        def error():
            self.error(error_messages['bounds'])
        
        limit_date(value, self.lower_limit, self.upper_limit, error)