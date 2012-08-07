from django.core.management.base import BaseCommand, CommandError

from piplmesh.panels.horoscope import tasks

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Manually update horoscopes with manage.py command.
        """
        
        if int(options['verbosity']) > 0:
            self.stdout.write('Start the update manually horoscopes. Please wait ...')
            self.stdout.write('\n\r')
        
        tasks.update_horoscope.delay()
        
        if int(options['verbosity']) > 0:
            self.stdout.write('Successfully updated all horoscope.')
            self.stdout.write('\n\r')