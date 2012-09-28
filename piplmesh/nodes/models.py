from piplmesh import nodes

NODE_ID_SEPARATOR = '-'

class Node(object):
    def __init__(self, id, name, location, latitude, longitude, url):
        self.id = id
        self.name = name
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.url = url

        self._outside_request = False

    def is_outside_request(self):
        return self._outside_request

    def is_inside_request(self):
        return not self._outside_request

    def get_full_node_id(self):
        return '%s%s%s' % (self.backend.get_full_name(), NODE_ID_SEPARATOR, self.id)

    @classmethod
    def parse_full_node_id(cls, full_node_id):
        return full_node_id.split(NODE_ID_SEPARATOR, 1)
