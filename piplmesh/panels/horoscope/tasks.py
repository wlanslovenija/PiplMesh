from __future__ import absolute_import

from celery import task

from . import models, providers

@task.task
def update_horoscope():
    """
    Task which updates horoscopes for all supported languages.

    Old horoscopes are left in the database.
    """

    for horoscope_provider in providers.get_all_providers():
        for sign in models.HOROSCOPE_SIGNS_DICT:
            horoscope_data = horoscope_provider.fetch_data(sign)

            models.Horoscope.objects(date=horoscope_data['date'], language=horoscope_provider.get_language(), sign=sign).update(set__forecast=horoscope_data['forecast'], upsert=True)