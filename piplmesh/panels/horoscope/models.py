from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import mongoengine

HOROSCOPE_SIGNS = (
    ('aries', _("Aries")),
    ('pisces', _("Pisces")),
    ('taurus', _("Taurus")),
    ('gemini', _("Gemini")),
    ('cancer', _("Cancer")),
    ('leo', _("Leo")),
    ('virgo', _("Virgo")),
    ('libra', _("Libra")),
    ('scorpio', _("Scorpio")),
    ('sagittarius', _("Sagittarius")),
    ('capricorn', _("Capricorn")),
    ('aquarius', _("Aquarius")),
)

HOROSCOPE_SIGNS_DICT = dict(HOROSCOPE_SIGNS)

class Horoscope(mongoengine.Document):
    date = mongoengine.DateTimeField(required=True, unique_with=('language', 'sign'))
    language = mongoengine.StringField(choices=settings.LANGUAGES, required=True, unique_with=('date', 'sign'))
    sign = mongoengine.StringField(choices=HOROSCOPE_SIGNS, required=True, unique_with=('date', 'language'))
    forecast = mongoengine.StringField(required=True)
    meta = {
        'indexes': ['date', 'language', 'sign']
    }