import datetime

from django import template
from django.contrib import auth
from django.test import client, signals
from django.utils import functional, translation

from tastypie_mongoengine import test_runner

from . import models, panel, providers, tasks

class BasicTest(test_runner.MongoEngineTestCase):
    @classmethod
    def setUpClass(cls):
        super(BasicTest, cls).setUpClass()

        # We fetch data, store it away, and delete
        tasks.update_horoscope()
        cls._horoscope_data = list(models.Horoscope.objects())
        models.Horoscope.drop_collection()

        for d in cls._horoscope_data:
            # So that data can be reinserted
            d.pk = None

        # So that django_browserid logging does not complain when doing auth.authenticate
        import logging
        logging.disable(logging.CRITICAL)

    def setUp(self):
        self.factory = client.RequestFactory()
        self.language = translation.get_language()

        models.Horoscope.objects.insert(self._horoscope_data, load_bulk=False, safe=True)

    def tearDown(self):
        translation.activate(self.language)

    def _request(self):
        request = self.factory.get('/')
        request.session = {}
        request.user = auth.authenticate(request=request)
        return request

    def _render(self, request):
        context = template.RequestContext(request)

        data = {}
        on_template_render = functional.curry(client.store_rendered_templates, data)
        signals.template_rendered.connect(on_template_render, dispatch_uid='template-render')

        try:
            rendered = panel.HoroscopePanel().render(request, context)
        finally:
            signals.template_rendered.disconnect(dispatch_uid='template-render')

        return data, rendered

    def test_horoscope_esperanto(self):
        # We assume here that we do not have horoscope in Esperanto

        translation.activate('eo')

        request = self._request()

        request.user.birthdate = datetime.date(1990, 1, 1)
        request.user.save()

        data, rendered = self._render(request)

        try:
            self.assertEqual(data['context']['error_language'], True)
        except KeyError:
            print data, rendered
            raise

    def test_horoscope_slovenian(self):
        translation.activate('sl')

        request = self._request()
        data, rendered = self._render(request)

        try:
            self.assertEqual(data['context']['error_birthdate'], True)
        except KeyError:
            print data, rendered
            raise

        # TODO: Go over all signs
        request.user.birthdate = datetime.date(1990, 1, 1)
        request.user.save()

        data, rendered = self._render(request)

        try:
            self.assertEqual(translation.force_unicode(data['context']['horoscope_source_url']), providers.get_provider('sl').get_source_url())
            self.assertEqual(translation.force_unicode(data['context']['horoscope_sign']), translation.force_unicode(models.HOROSCOPE_SIGNS_DICT['aquarius']))
        except KeyError:
            print data, rendered
            raise

    def test_horoscope_english(self):
        translation.activate('en')

        request = self._request()
        data, rendered = self._render(request)

        try:
            self.assertEqual(data['context']['error_birthdate'], True)
        except KeyError:
            print data, rendered
            raise

        # TODO: Go over all signs
        request.user.birthdate = datetime.date(1990, 1, 1)
        request.user.save()

        data, rendered = self._render(request)

        try:
            self.assertEqual(translation.force_unicode(data['context']['horoscope_source_url']), providers.get_provider('en').get_source_url())
            self.assertEqual(translation.force_unicode(data['context']['horoscope_sign']), translation.force_unicode(models.HOROSCOPE_SIGNS_DICT['aquarius']))
        except KeyError:
            print data, rendered
            raise
