import os, pkgutil

from django.utils import importlib

# A fake panel module which loads all bundled panels instead

for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    if module in ('models', 'panel', 'tasks'):
        # Prevent failing because of circular imports (models imports panel)
        continue

    for file in ('panel', 'models', 'tasks'):
        try:
            importlib.import_module('.%s.%s' % (module, file), 'piplmesh.panels')
        except ImportError, e:
            message = str(e)
            if message != 'No module named %s' % (file,):
                raise
