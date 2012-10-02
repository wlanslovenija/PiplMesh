import datetime

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from missing import timezone

import mongoengine

GENDER_CHOICES = (
    ('male', _("male")),
    ('female', _("female")),
)

ERROR_MESSAGES = {
    'bounds': _("Value is out of bounds."),
    'callable': _("Callable did not return datetime.date or datetime.datetime object."),
}

def limit_date(value, lower_limit, upper_limit, error):
    if not value:
        return

    if upper_limit:
        tmp_value = value
        if callable(upper_limit):
            tmp_upper_limit = upper_limit()
            if not isinstance(tmp_upper_limit, (datetime.datetime, datetime.date)):
                error('callable')
        else:
            tmp_upper_limit = upper_limit

        # If one object doesn't contain time (is date type), convert the other one to date object
        if not isinstance(tmp_value, datetime.datetime) or not isinstance(tmp_upper_limit, datetime.datetime):
            if isinstance(tmp_upper_limit, datetime.datetime):
                tmp_upper_limit = timezone.to_date(tmp_upper_limit)
            elif isinstance(tmp_value, datetime.datetime):
                tmp_value = timezone.to_date(tmp_value)

        if tmp_value > tmp_upper_limit:
            error('bounds')

    if lower_limit:
        tmp_value = value
        if callable(lower_limit): 
            tmp_lower_limit = lower_limit()
            if not isinstance(tmp_lower_limit, (datetime.datetime, datetime.date)):
                error('callable')
        else:
            tmp_lower_limit = lower_limit

        # If one object doesn't contain time (is date type), convert the other one to date object
        if not isinstance(tmp_value, datetime.datetime) or not isinstance(tmp_lower_limit, datetime.datetime):
            if isinstance(tmp_lower_limit, datetime.datetime):
                tmp_lower_limit = timezone.to_date(tmp_lower_limit)
            elif isinstance(tmp_value, datetime.datetime):
                tmp_value = timezone.to_date(tmp_value)

        if tmp_value < tmp_lower_limit:
            error('bounds')

class LanguageField(mongoengine.StringField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 5)
        kwargs.setdefault('choices', settings.LANGUAGES)
        kwargs.setdefault('default', settings.LANGUAGE_CODE)

        super(LanguageField, self).__init__(*args, **kwargs)

class GenderField(mongoengine.StringField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 6)
        kwargs.setdefault('choices', GENDER_CHOICES)
        kwargs.setdefault('default', None)

        super(GenderField, self).__init__(*args, **kwargs)

class LimitedDateTimeField(mongoengine.DateTimeField):
    """
    A datetime field which can check also upper and lower limit arguments.
    """

    def __init__(self, upper_limit=None, lower_limit=None, *args, **kwargs):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        if self.upper_limit and not callable(self.upper_limit) and not isinstance(self.upper_limit, (datetime.datetime, datetime.date)):
            self.error(u"Invalid upper_limit argument.")
        if self.lower_limit and not callable(self.lower_limit) and not isinstance(self.lower_limit, (datetime.datetime, datetime.date)):
            self.error(u"Invalid lower_limit argument.")

        super(LimitedDateTimeField, self).__init__(*args, **kwargs)

    def validate(self, value):
        super(LimitedDateTimeField, self).validate(value)

        def error(message):
            self.error(ERROR_MESSAGES[message])

        limit_date(value, self.lower_limit, self.upper_limit, error)
