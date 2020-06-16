from django.core.management import call_command
from django.core.management.base import BaseCommand

from core.cli.mixins import CliInteractionMixin
from redmine import Redmine


class Command(BaseCommand, CliInteractionMixin):
    help = "Syncronizes all data to Redmine instance."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redmine = Redmine()

    def handle(self, *args, **options):
        print()
        self.stdout.write('VALIDATING REDMINE INSTANCE')
        print()

        if self.redmine.instance_valid() is False:
            self.stderr.write(self.style.ERROR('Errors:'))
            for e in self.redmine.instance_errors():
                self.stderr.write(self.style.ERROR(f'- {e}'))

            self.exit()

        call_command('sync_trackers')
        call_command('sync_score_field')
        call_command('sync_projects')
        call_command('sync_categories')
        call_command('sync_versions')
        call_command('sync_issues')
