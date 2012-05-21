from optparse import make_option

from django.conf import settings
from django.core.management import base

from mongoengine import connection

# We override Django's flush command with our own for MongoDB
# This makes also possible to run tests without relational
# database defined, because original flush command was
# throwing exceptions and preventing tests to be run

class Command(base.NoArgsCommand):
    option_list = base.NoArgsCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
        make_option('--database', action='store', dest='database',
            default=getattr(settings, 'MONGO_DATABASE_NAME', None), help='Nominates a database to flush. '
                'Defaults to the "settings.MONGO_DATABASE_NAME" database.'),
    )
    help = ('Flushes MongoDB database. This means that all data will be removed from the database.')

    def handle_noargs(self, **options):
        database = options.get('database')
        verbosity = int(options.get('verbosity'))
        interactive = options.get('interactive')

        if not database:
            raise base.CommandError("No MongoDB database specified.")

        if interactive:
            confirm = raw_input("""You have requested a flush of the database.
This will IRREVERSIBLY DESTROY all data currently in the '%s' database.
Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: """ % (database,))
        else:
            confirm = 'yes'

        if confirm == 'yes':
            try:
                db = connection.get_db()
                for collection in db.collection_names():
                    if collection == 'system.indexes':
                        continue
                    db.drop_collection(collection)
            except Exception, e:
                raise base.CommandError("""Database '%s' couldn't be flushed.
The full error: %s""" % (database, e))

            if verbosity > 1:
                self.stdout.write("Database '%s' flushed.\n" % (database,))

        else:
            print "Flush cancelled."
