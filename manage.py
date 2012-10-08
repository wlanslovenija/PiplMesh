#!/usr/bin/env python
import imp, os, sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'piplmesh.settings')

    from django.core import management

    original_get_commands = management.get_commands

    # We override get_commands with a version which loads automatically all management
    # commands from all panels so that it is not necessary to list panels manually
    # in INSTALLED_APPS to get their commands (which makes their tests being loaded twice)
    def get_commands():
        commands = original_get_commands()

        # Find and load the management module for all panels
        path = imp.find_module('piplmesh')[1]
        panels_directory = imp.find_module('panels', [path])[1]
        for directory in os.listdir(panels_directory):
            app_name = 'piplmesh.panels.%s' % directory
            try:
                path = management.find_management_module(app_name)
                commands.update(dict([(name, app_name) for name in management.find_commands(path)]))
            except ImportError:
                pass

        return commands

    management.get_commands = get_commands

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)