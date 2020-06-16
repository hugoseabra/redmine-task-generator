from django.core.management.base import BaseCommand

from apps.redmine_project.models import Project
from apps.redmine_settings.models import Tracker, CustomField
from core.cli.mixins import CliInteractionMixin
from redmine import Redmine
from redmine.project_settings import PROJECT_DEFAULT_MODULES


class Command(BaseCommand, CliInteractionMixin):
    help = "Synchronizes projects."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redmine = Redmine()

    def handle(self, *args, **options):
        print()
        self.stdout.write('SYNCHRONIZING PROJECTS')
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
        self.stdout.write('Redmine projects ...', ending='\r')
        projects = self.redmine.project.all()
        project_ids = [t.id for t in projects]
        num = len(project_ids)

        self.stdout.write(
            'Redmine projects found: {}'.format(self.style.SUCCESS(num))
        )
        print()

        for item in projects:
            Project.objects.get_or_create(
                name=item.name,
                redmine_id=item.identifier,
                slug=item.identifier,
            )
            name = self.get_normalized_name(item.name, 20)
            msg = f' - {name} (ID: {item.id})'
            self.stdout.write(self.style.SUCCESS(msg))

    def sync_out(self):
        tracker_ids = [t.redmine_id for t in Tracker.objects.all()]
        custom_field_ids = [c.redmine_id for c in CustomField.objects.all()]

        print()
        self.stdout.write('Internal projects ...', ending='\r')

        qs = Project.objects.filter(redmine_id__isnull=True)
        num = qs.count()

        self.stdout.write(
            'Internal projects found: {}'.format(self.style.SUCCESS(
                num or '0'
            ))
        )
        print()

        for p in qs:
            redmine = self.redmine.project.create(
                name=p.name,
                identifier=p.slug,
                tracker_ids=tracker_ids,
                issue_custom_field_ids=custom_field_ids,
                enabled_module_names=PROJECT_DEFAULT_MODULES,
            )
            p.redmine_id = redmine.id
            p.save()

            name = self.get_normalized_name(p.name, 20)
            msg = f' - {name} (ID: {p.redmine_id})'
            self.stdout.write(self.style.SUCCESS(msg))
