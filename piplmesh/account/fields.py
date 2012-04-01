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
    def validate(self, value):
        super(LimitedDateTimeField, self).validate(value)
        
        try:
            futureDate = value > datetime.datetime.today() - datetime.timedelta(settings.FUTUREDATE)
        except:
            futureDate = value > datetime.date.today() - datetime.timedelta(settings.FUTUREDATE)
        if futureDate:
            self.error(u'User born on "%s" is too young to register' % value)