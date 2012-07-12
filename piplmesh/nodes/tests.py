from __future__ import absolute_import
from pprint import pprint
import random

from django.test import client, utils

from piplmesh import nodes, test_runner
from piplmesh.nodes import data
from piplmesh.nodes.backends import NodesBackend

@utils.override_settings(NODES_BACKENDS=('piplmesh.nodes.backends.NodesBackend',))
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



    def test_get_closest_node(self):
        node_backend = NodesBackend()
        for i in range(10):
            node1 = data.nodes[i]

            node2 = node_backend.get_closest_node(1,node1.latitude, node1.longitude)

            self.assertEquals(node1.latitude, node2.latitude)
            self.assertEquals(node1.longitude, node2.longitude)
            self.assertEquals(node1.id, node2.id)
