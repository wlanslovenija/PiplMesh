from __future__ import absolute_import

from django.test import client, utils

from tastypie_mongoengine import test_runner

from piplmesh import nodes

@utils.override_settings(NODES_BACKENDS=('piplmesh.nodes.backends.RandomNodesBackend',))
class BasicTest(test_runner.MongoEngineTestCase):
    def setUp(self):
        self.factory = client.RequestFactory()

    def test_get_node(self):
        request = self.factory.get('/')
        request.session = {}

        node1 = nodes.get_node(request)
        self.assertNotEqual(node1, None)

        node2 = nodes.get_node(request)
        self.assertEqual(node1.id, node2.id)
