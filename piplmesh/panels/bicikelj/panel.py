from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

from . import stations

class BicikeljPanel(panels.BasePanel):
    def get_context(self, context):
        context.update({
            'header': _("Bicikelj stations"),
            # We convert iterator to list so that content is available when testing
            'stations': list(stations.get_stations_nearby(self.request.node.latitude, self.request.node.longitude)),
        })
        return context

panels.panels_pool.register(BicikeljPanel)