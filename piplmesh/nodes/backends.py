from __future__ import absolute_import

import copy, random

from . import data
from piplmesh.nodes import distance

class NodesBackend(object):

    def get_source_node(self, request):
        """
        Returns random node for now.
        """

        return self.get_random_node()


    def get_random_node(self):

        node_id = random.randrange(len(data.nodes))
        node = copy.copy(data.nodes[node_id])
        node.id = node_id

        return node


    def get_closest_node(self, request, latitude, longitude):

        t = (-1,-1)

        for i,n in enumerate(data.nodes):
            dist = (i, distance(n.latitude, n.longitude, latitude, longitude))
            if(dist[1] < t[1] or t[0] == -1):
                t = dist
        node = copy.copy(data.nodes[t[0]])
        node.node_id = t[0]

        return node

    def get_node(self, node_id):
        try:
            node = copy.copy(data.nodes[node_id])
            node.id = node_id
            return node
        except IndexError:
            return None

    def get_all_nodes(self):
        for i, node in enumerate(data.nodes):
            node = copy.copy(node)
            node.id = i
            yield node
