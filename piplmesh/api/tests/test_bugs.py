import datetime

from tastypie_mongoengine import test_runner

import pytz

from django.utils import timezone, translation

from tastypie.utils import formatting

class BugsTest(test_runner.MongoEngineTestCase):
    def test_format_date(self):
        paris_tz = pytz.timezone('Europe/Paris')
        d = paris_tz.localize(datetime.datetime(2012, 3, 3, 1, 30))

        tz = timezone.get_current_timezone()
        timezone.activate(pytz.timezone('America/New_York'))

        lang = translation.get_language()
        translation.activate('sl')

        try:
            self.assertEqual(formatting.format_datetime(d), 'Sat, 03 Mar 2012 01:30:00 +0100')
        finally:
            timezone.activate(tz)
            translation.activate(lang)