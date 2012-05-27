from __future__ import absolute_import

from django.test import client, utils

from piplmesh import nodes, test_runner

@utils.override_settings(NODES_BACKENDS=('piplmesh.nodes.backends.RandomNodesBackend',))
class BasicTest(test_runner.MongoEngineTestCase):
    def setUp(self):
        self.factory = client.RequestFactory()

    def test_source_node(self):
        request = self.factory.get('/')
        request.session = {}

        # We cannot really test anything smart except that it runs successfully
        node1 = nodes.get_source_node(request)

        node2 = nodes.get_source_node(request)
        self.assertEqual(node1, node2)

    def test_closest_node(self):
        request = self.factory.get('/')
        request.session = {}

        node1 = nodes.get_closest_node(request, 0, 0)
        self.assertNotEqual(node1, None)

        node2 = nodes.get_closest_node(request, 0, 0)
        self.assertEqual(node1, node2)
