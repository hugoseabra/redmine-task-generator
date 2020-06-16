from django.core.management.base import BaseCommand

from apps.redmine_settings.models import Tracker
from core.cli.mixins import CliInteractionMixin
from redmine import Redmine


class Command(BaseCommand, CliInteractionMixin):
    help = "Synchronizes trackers."

    def handle(self, *args, **options):
        redmine = Redmine()

        print()

        self.stdout.write('Trackers ...', ending='\r')
        trackers = redmine.tracker.all()
        num = len(trackers)

        self.stdout.write('Trackers found: {}'.format(
            self.style.SUCCESS(num or '0')
        ))

        for t in trackers:
            tracker, _ = Tracker.objects.get_or_create(name=t.name,
                                                       redmine_id=t.id)

            tracker_msg = f'\t- {t.name} (ID: {t.id})'
            self.stdout.write(self.style.SUCCESS(tracker_msg))

        print()
