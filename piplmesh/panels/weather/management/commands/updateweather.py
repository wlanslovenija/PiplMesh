from django.core.management import base

from piplmesh.panels.weather import tasks

class Command(base.BaseCommand):
    help = 'Force weather update.'

    def handle(self, *args, **options):
        """
        Forces Weather update.
        """

        verbosity = int(options['verbosity'])

        if verbosity > 1:
            self.stdout.write("Updating weather...\n")

        tasks.generate_weather_tasks.delay().wait()

        if verbosity > 1:
            self.stdout.write("Successfully updated weather.\n")
