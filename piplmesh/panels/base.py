import collections

from django.template import loader

from . import exceptions

class BasePanel(object):
    template = None
    name = None
    dependencies = ()

    def __init__(self):
        # To prevent import cycle
        from . import panels_pool

        for dependency in self.get_dependencies():
            if not panels_pool.panels_pool.has_panel(dependency):
                raise exceptions.PanelDependencyNotRegistered("Panel '%s' depends on panel '%s', but the latter is not registered" % (self.get_name(), dependency))

    @classmethod
    def get_name(cls):
        if cls.name:
            return cls.name

        # TODO: This removes Panel everywhere, not just when a suffix
        return cls.__name__.replace('Panel', '').lower()

    @classmethod
    def get_dependencies(cls):
        return cls.dependencies

    def get_template(self):
        templates = []

        if self.template:
            if isinstance(self.template, collections.Iterable):
                templates.extend(self.template)
            else:
                templates.append(self.template)

        templates.append('panel/%s/panel.html' % (self.get_name()))
        templates.append('panel/panel.html')

        return templates

    def get_context(self, context):
        context.update({
            'name': self.get_name()
        })
        
        return context

    def render(self, request, context):
        try:
            self.request = request
            template = self.get_template()
            context.update(self.get_context({}))
            try:
                return loader.render_to_string(template, context)
            finally:
                context.pop()
        finally:
            self.request = None
