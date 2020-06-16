from django.core.management.base import BaseCommand

from apps.redmine_settings.models import Tracker, CustomField
from core.cli.mixins import CliInteractionMixin
from redmine import Redmine


class Command(BaseCommand, CliInteractionMixin):
    help = "Synchronizes score field as custom field."

    def handle(self, *args, **options):

        redmine = Redmine()

        print()
        self.stdout.write('Score field ...', ending='\r')

        if redmine.instance_valid() is False:
            self.stderr.write('Score field not found or invalid:')
            for m in redmine.validator.score_field_errors:
                self.stderr.write(f'- {m}')

            self.exit()

        field = redmine.score_field

        if field is None:
            print(redmine.validator.score_field_errors)
            self.exit()

        instance, _ = CustomField.objects.get_or_create(
            name=field.name,
            redmine_id=field.id,
        )
        instance.possible_values = field.possible_values
        instance.save()

        self.stdout.write('Score field: {}'.format(self.style.SUCCESS('OK')))

        print()

