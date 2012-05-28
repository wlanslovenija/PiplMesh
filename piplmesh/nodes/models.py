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
