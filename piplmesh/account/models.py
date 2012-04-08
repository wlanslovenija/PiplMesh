import datetime

from django.utils.translation import ugettext_lazy as _

import mongoengine
from mongoengine.django import auth

from piplmesh.account import fields

# rough lower limit date
LOWER_DATE_LIMIT = 366 * 120

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

class User(auth.User):
    birthdate = fields.LimitedDateTimeField(upper_limit=datetime.datetime.today(), lower_limit=datetime.datetime.today() - datetime.timedelta(LOWER_DATE_LIMIT))
    gender = fields.GenderField()
    language = fields.LanguageField()
    
    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)