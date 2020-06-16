from django.core.management.base import BaseCommand
from redminelib.exceptions import ForbiddenError

from apps.redmine_project.models import Project, Category
from core.cli.mixins import CliInteractionMixin
from redmine import Redmine


class Command(BaseCommand, CliInteractionMixin):
    help = "Synchronizes categories."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redmine = Redmine()

    def handle(self, *args, **options):
        print()
        self.stdout.write('SYNCHRONIZING CATEGORIES')
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

            self.stdout.write('Redmine categories ...', ending='\r')
            try:
                cats = self.redmine.issue_category.filter(
                    project_id=p.redmine_id
                )
                num = len(cats)

                self.stdout.write(
                    'Redmine categories found: {}'.format(
                        self.style.SUCCESS(num or '0')
                    )
                )

                for item in cats:
                    cat, _ = Category.objects.get_or_create(
                        name=item.name,
                        project_id=str(p.pk),
                        redmine_id=item.id
                    )

                    name = self.get_normalized_name(cat.name, 20)
                    msg = f' - {name} (ID: {cat.redmine_id})'
                    self.stdout.write(self.style.SUCCESS(msg))

            except ForbiddenError:
                self.stdout.write('Redmine categories: {}'.format(
                    self.style.SUCCESS('not supported')
                ))

            print('--------')

    def sync_out(self):
        print()
        self.stdout.write('Internal categories ...', ending='\r')

        qs = Category.objects.filter(redmine_id__isnull=True)
        num = qs.count()

        self.stdout.write(
            'Internal categories found: {}'.format(self.style.SUCCESS(
                num or '0'
            ))
        )
        print()

        for i in qs:
            redmine = self.redmine.issue_category.create(
                name=i.name,
                project_id=i.project.redmine_id,
            )
            i.redmine_id = redmine.id
            i.save()

            name = self.get_normalized_name(i.name, 20)
            msg = f' - {name} (ID: {i.redmine_id})'
            self.stdout.write(self.style.SUCCESS(msg))
