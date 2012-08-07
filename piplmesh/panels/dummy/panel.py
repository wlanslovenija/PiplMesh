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

class DummyPanel2(panels.BasePanel):
    def get_context(self, context):
        context.update({
            'header': _("Dummy panel 2"),
            'content': '\n\n'.join(lorem_ipsum.paragraphs(random.randint(1, 1))),
            'id': 'dummy2',
        })
        return context

class DummyPanel3(panels.BasePanel):
    def get_context(self, context):
        context.update({
            'header': _("Dummy panel 3"),
            'content': '\n\n'.join(lorem_ipsum.paragraphs(random.randint(1, 1))),
            'id': 'dummy3',
        })
        return context

class DummyPanel4(panels.BasePanel):
    def get_context(self, context):
        context.update({
            'header': _("Dummy panel 4"),
            'content': '\n\n'.join(lorem_ipsum.paragraphs(random.randint(1, 1))),
            'id': 'dummy4',
        })
        return context

if settings.DEBUG:
    panels.panels_pool.register(DummyPanel)
    panels.panels_pool.register(DummyPanel2)
    panels.panels_pool.register(DummyPanel3)
    panels.panels_pool.register(DummyPanel4)
