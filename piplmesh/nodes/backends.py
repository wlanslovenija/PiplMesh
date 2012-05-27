from __future__ import absolute_import

import random

from . import data

class RandomNodesBackend(object):
    def get_source_node(self, request):
        """
        Returns with 0.2 probability None or selects one node at random.
        """

        if random.random() < 0.2:
            return None
        else:
            node_id = random.randrange(len(data.nodes))
            node = data.nodes[node_id]
            node.id = node_id
            return node

    def get_closest_node(self, request, latitude, longitude):
        """
        Because searching for real closest node is complex,
        it just returns a random node.
        """

        node_id = random.randrange(len(data.nodes))
        node = data.nodes[node_id]
        node.id = node_id
        return node

    def get_node(self, node_id):
        try:
            return data.nodes[node_id]
        except IndexError:
            return None
