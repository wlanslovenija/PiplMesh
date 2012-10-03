from __future__ import absolute_import

from celery import task
from celery.task import schedules

from . import models, providers
from piplmesh.utils import decorators

CHECK_FOR_NEW_HOROSCOPE = 6 # am every day

@task.periodic_task(run_every=schedules.crontab(hour=CHECK_FOR_NEW_HOROSCOPE))
@decorators.single_instance_task()
def update_horoscope():
    """
    Task which updates horoscopes for all supported languages.

    Old horoscopes are left in the database.
    """

    for horoscope_provider in providers.get_all_providers():
        for sign in models.HOROSCOPE_SIGNS_DICT:
            horoscope_data = horoscope_provider.fetch_data(sign)

            models.Horoscope.objects(date=horoscope_data['date'], language=horoscope_provider.get_language(), sign=sign).update(set__forecast=horoscope_data['forecast'], upsert=True)