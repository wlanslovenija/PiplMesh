from __future__ import absolute_import

import copy, random

from . import data

class RandomNodesBackend(object):
    def get_source_node(self, request):
        """
        Returns a node at random.
        """

        node_id = random.randrange(len(data.nodes))
        node = copy.copy(data.nodes[node_id])
        node.id = node_id
        return node

    def get_closest_node(self, request, latitude, longitude):
        """
        Because searching for real closest node is complex,
        it just returns a random node.
        """

        node_id = random.randrange(len(data.nodes))
        node = copy.copy(data.nodes[node_id])
        node.id = node_id
        return node

    def get_node(self, node_id):
        try:
            node = copy.copy(data.nodes[int(node_id)])
            node.id = node_id
            return node
        except IndexError:
            return None

    def get_all_nodes(self):
        for i, node in enumerate(data.nodes):
            node = copy.copy(node)
            node.id = i
            yield node

    def get_full_name(self):
        return "%s.%s" % (self.__module__, self.__class__.__name__)
