import os, sys

from django.template import base, loader
from django.template.loaders import app_directories

from ... import panels

fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()

app_template_dirs = list(app_directories.app_template_dirs)
for panel in panels.panels_pool.get_all_panels():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(sys.modules[panel.__module__].__file__), 'templates'))
    if os.path.isdir(template_dir):
        app_template_dirs.append(template_dir.decode(fs_encoding))
app_directories.app_template_dirs = tuple(app_template_dirs)

# This loader is not really used, we just define it to change app_template_dirs of app_directories loader
class Loader(loader.BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        raise base.TemplateDoesNotExist(template_name)


























