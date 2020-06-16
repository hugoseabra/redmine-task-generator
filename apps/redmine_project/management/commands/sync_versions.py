from django.core.management.base import BaseCommand
from redminelib.exceptions import ForbiddenError

from apps.redmine_project.models import Project, Version
from core.cli.mixins import CliInteractionMixin
from redmine import Redmine


class Command(BaseCommand, CliInteractionMixin):
    help = "Synchronizes versions."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redmine = Redmine()

    def handle(self, *args, **options):
        print()
        self.stdout.write('SYNCHRONIZING VERSIONS')
        print()

        self.sync_in()
        self.sync_out()

    def get_normalized_name(self, name, max_length):
        length = len(name)
        diff_length = max_length - 3

        if length > diff_length:
            name = name[:diff_length] + '...'
        else:
            suffix = ' ' * (20 - length)
            name = name + suffix

        return name

    def sync_in(self):
        for p in Project.objects.all():

            self.stdout.write('Project: {}'.format(self.style.SUCCESS(p.name)))

            self.stdout.write('Redmine versions ...', ending='\r')
            try:
                versions = self.redmine.version.filter(project_id=p.redmine_id)
                num = len(versions)

                self.stdout.write(
                    'Redmine versions found: {}'.format(
                        self.style.SUCCESS(num or '0')
                    )
                )

                for item in versions:
                    version, _ = Version.objects.get_or_create(
                        redmine_id=item.id,
                        project_id=str(p.pk),
                    )
                    version.name = item.name
                    version.status = item.status
                    version.description = item.description

                    if hasattr(item,'due_date'):
                        version.due_date = item.due_date

                    version.save()

                    name = self.get_normalized_name(version.name, 20)
                    msg = f' - {name} (ID: {version.redmine_id})'
                    self.stdout.write(self.style.SUCCESS(msg))

            except ForbiddenError:
                self.stdout.write('Redmine versions: {}'.format(
                    self.style.SUCCESS('not supported')
                ))

            print('--------')

    def sync_out(self):
        print()
        self.stdout.write('Internal versions ...', ending='\r')

        qs = Version.objects.filter(redmine_id__isnull=True)
        num = qs.count()

        self.stdout.write(
            'Internal versions found: {}'.format(self.style.SUCCESS(
                num or '0'
            ))
        )
        print()

        for i in qs:
            redmine = self.redmine.version.create(
                name=i.name,
                due_date=i.due_date,
                description=i.description,
                status=i.status or 'open',
                project_id=i.project.redmine_id,
            )
            i.redmine_id = redmine.id
            i.save()

            name = self.get_normalized_name(i.name, 20)
            msg = f' - {name} (ID: {i.redmine_id})'
            self.stdout.write(self.style.SUCCESS(msg))
