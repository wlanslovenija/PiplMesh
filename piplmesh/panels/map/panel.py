from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

class MapPanel(panels.BasePanel):
    def get_context(self, context):
        context.update({
            'header': _("Map"),
        })
        return context

panels.panels_pool.register(MapPanel)
