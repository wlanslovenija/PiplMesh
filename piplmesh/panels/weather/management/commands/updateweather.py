import time

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

        results = tasks.generate_weather_tasks()
        prev_completed = None
        while not results.ready():
            completed = results.completed_count()
            if prev_completed != completed:
                self.stdout.write("Completed %d/%d.\n" % (completed, len(results)))
                prev_completed = completed
            time.sleep(1)

        if verbosity > 1:
            self.stdout.write("Successfully updated weather.\n")