import itertools

from django import template
from django.test import client, signals
from django.utils import functional

from tastypie_mongoengine import test_runner

from . import models, panel, tasks
from piplmesh import nodes

class BasicTest(test_runner.MongoEngineTestCase):
    @classmethod
    def setUpClass(cls):
        super(BasicTest, cls).setUpClass()

        # We fetch data, store it away, and delete
        tasks.update_station_info()
        cls._bicikelj_data = list(models.BicikeljStation.objects())
        models.BicikeljStation.drop_collection()

        for d in cls._bicikelj_data:
            # So that data can be reinserted
            d.pk = None

    def setUp(self):
        self.factory = client.RequestFactory()

        models.BicikeljStation.objects.insert(self._bicikelj_data, load_bulk=False, safe=True)

    def test_bicikelj(self):
        node = next(itertools.islice(nodes.get_all_nodes(), 12, 13))

        self.assertEqual(node.name, 'fri')

        request = self.factory.get('/')
        request.session = {
            nodes.SESSION_KEY: node.id,
            nodes.BACKEND_SESSION_KEY: node.backend.get_full_name(),
        }
        request.node = nodes.get_node(request)

        self.assertEqual(node.id, request.node.id)

        context = template.RequestContext(request)

        data = {}
        on_template_render = functional.curry(client.store_rendered_templates, data)
        signals.template_rendered.connect(on_template_render, dispatch_uid="template-render")

        try:
            panel.BicikeljPanel().render(request, context)
        finally:
            signals.template_rendered.disconnect(dispatch_uid="template-render")

        self.assertEqual(len(data['context']['stations']), 1)
