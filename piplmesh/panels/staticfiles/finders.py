from django.conf import settings
from django.contrib.staticfiles import finders

from ... import panels

class PanelsDirectoriesFinder(finders.AppDirectoriesFinder):
    def __init__(self, apps=None, *args, **kwargs):
        if apps is None:
            apps = list(settings.INSTALLED_APPS)

            for panel in panels.panels_pool.get_all_panels():
                try:
                    module, _ = panel.__module__.rsplit('.', 1)
                    apps.append(module)
                except ValueError:
                    pass

            apps = tuple(apps)

        super(PanelsDirectoriesFinder, self).__init__(apps, *args, **kwargs)
