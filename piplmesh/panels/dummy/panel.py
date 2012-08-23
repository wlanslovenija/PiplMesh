import random

from django.conf import settings
from django.contrib.webdesign import lorem_ipsum
from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

class DummyPanel(panels.BasePanel):
    def get_context(self, context):
        context.update({
            'header': _("Dummy panel"),
            'content': '\n\n'.join(lorem_ipsum.paragraphs(random.randint(1, 1))),
            'id': 'dummy',
        })
        return context

if settings.DEBUG:
    panels.panels_pool.register(DummyPanel)
