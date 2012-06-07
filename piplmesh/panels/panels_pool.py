from __future__ import absolute_import

from django.conf import settings
from django.utils import importlib

from . import base, exceptions

class PanelsPool(object):
    def __init__(self):
        self.panels = {}
        self.discovered = False

    def discover_panels(self):
        if self.discovered:
            return
        self.discovered = True

        for app in settings.INSTALLED_APPS:
            try:
                importlib.import_module('.panel', app)
            except ImportError, e:
                message = str(e)
                if message != 'No module named panel':
                    raise

    def register(self, panel_or_iterable):
        if not hasattr(panel_or_iterable, '__iter__'):
            panel_or_iterable = [panel_or_iterable]

        for panel in panel_or_iterable:
            if not issubclass(panel, base.BasePanel):
                raise exceptions.PanelHasInvalidBase("'%s' is not a subclass of piplmesh.panels.BasePanel" % panel.__name__)

            panel_name = panel.get_name()

            if panel_name in self.panels:
                raise exceptions.PanelAlreadyRegistered("A panel with name '%s' is already registered" % panel_name)

            self.panels[panel_name] = panel

    def unregister(self, panel_or_iterable):
        if not hasattr(panel_or_iterable, '__iter__'):
            panel_or_iterable = [panel_or_iterable]

        for panel in panel_or_iterable:
            panel_name = panel.get_name()

            if panel_name not in self.panels:
                raise exceptions.PanelNotRegistered("No panel with name '%s' is registered" % panel_name)

            del self.panels[panel_name]

    def get_all_panels(self):
        self.discover_panels()

        return [panel for (_, panel) in sorted(self.panels.items())]

    def get_panel(self, panel_name):
        self.discover_panels()

        try:
            return self.panels[panel_name]
        except KeyError:
            raise exceptions.PanelNotRegistered("No panel with name '%s' is registered" % panel_name)

    def has_panel(self, panel_name):
        self.discover_panels()

        return panel_name in self.panels

panels_pool = PanelsPool()
