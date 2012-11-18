from django.core.management import base

from piplmesh.panels.horoscope import tasks

class Command(base.BaseCommand):
    help = 'Force horoscopes update.'

    def handle(self, *args, **options):
        """
        Forces horoscopes update.
        """

        verbosity = int(options['verbosity'])

        if verbosity > 1:
            self.stdout.write("Updating horoscopes...\n")

        tasks.update_horoscope.delay().wait()

        if verbosity > 1:
            self.stdout.write("Successfully updated all horoscopes.\n")
