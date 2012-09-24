from __future__ import absolute_import

import datetime

from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

from . import models, providers

HOROSCOPE_OBSOLETE = 2 # days

class HoroscopePanel(panels.BasePanel):
    def get_context(self, context):
        context = super(HoroscopePanel, self).get_context(context)
        user = self.request.user

        context.update({
            'header': _("Today's horoscope"),
        })

        if not user.birthdate:
            context.update({
                'error_birthdate': True,
            })
            return context

        try:
            provider = providers.get_provider(translation.get_language())
        except KeyError:
            context.update({
                'error_language': True,
            })
            return context

        user_sign = providers.get_horoscope_sign(user.birthdate.day, user.birthdate.month)

        try:
            horoscope = models.Horoscope.objects(
                language=translation.get_language(),
                sign=user_sign,
            ).order_by('-date').first()
        except models.Horoscope.DoesNotExist:
            context.update({
                'error_data': True,
            })
            return context
        
        if horoscope is None:
            context.update({
                'error_data': True,
            })
            return context

        if timezone.now() > horoscope.date + datetime.timedelta(days=HOROSCOPE_OBSOLETE):
            context.update({
                'error_obsolete': True,
            })
            return context

        context.update({
            'horoscope_forecast': horoscope.forecast,
            'horoscope_sign': models.HOROSCOPE_SIGNS_DICT[user_sign],
            'horoscope_date': horoscope.date,
            'horoscope_source_name': provider.get_source_name(),
            'horoscope_source_url': provider.get_source_url(),
        })

        return context

panels.panels_pool.register(HoroscopePanel)
