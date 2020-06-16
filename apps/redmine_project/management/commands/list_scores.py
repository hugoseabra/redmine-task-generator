from django.core.management.base import BaseCommand

from core.cli.mixins import CliInteractionMixin
from redmine import Redmine


class Command(BaseCommand, CliInteractionMixin):
    help = "List scores."

    def handle(self, *args, **options):
        print()
        self.stdout.write('Score values')
        print()

        from redmine.scores import SCORES

        for _, score in SCORES.items():
            for k, v in score.items():
                self.stdout.write(f'{k}. {v}')
