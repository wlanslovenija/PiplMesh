from django.core.management.base import BaseCommand, CommandError

from piplmesh.panels.horoscope import tasks

class Command(BaseCommand):
    help = 'Manually update horoscopes.'

    def handle(self, *args, **options):
        """
        Manually update horoscopes with manage.py command.
        """

        if int(options['verbosity']) > 1:
            self.stdout.write('Start the update manually horoscopes. Please wait ...\n')

        result = tasks.update_horoscope.delay()
        result.wait()

        if result.ready():
            if int(options['verbosity']) > 1:
                self.stdout.write('Successfully updated all horoscope.\n')
        else:
            if int(options['verbosity']) > 1:
                self.stdout.write('Failure on updating horoscopes.\n')