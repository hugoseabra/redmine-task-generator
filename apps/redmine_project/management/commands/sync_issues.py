from django.core.management.base import BaseCommand
from redminelib.exceptions import ForbiddenError

from apps.redmine_project.models import Project, Issue, Version
from apps.redmine_settings.models import Tracker, CustomField
from core.cli.mixins import CliInteractionMixin
from redmine import Redmine
from redmine.scores import SCORE_CARD_FIELD_NAME


class Command(BaseCommand, CliInteractionMixin):
    help = "Synchronizes issues."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redmine = Redmine()
        self.score_field_name = SCORE_CARD_FIELD_NAME

    def handle(self, *args, **options):
        print()
        self.stdout.write('SYNCHRONIZING ISSUES')
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
            self.stdout.write('Redmine issues ...', ending='\r')

            redmine_project = self.redmine.project.get(p.redmine_id)

            try:
                issues = redmine_project.issues
                num = len(issues)

                self.stdout.write(
                    'Redmine issues found: {}'.format(
                        self.style.SUCCESS(num or '0')
                    )
                )
                for item in issues:
                    tracker = Tracker.objects.get(redmine_id=item.tracker.id)

                    version = None
                    if hasattr(item, 'fixed_version_id'):
                        try:
                            version = Version.objects.get(
                                redmine_id=item.fixed_version_id
                            )
                        except Version.DoesNotExist:
                            pass

                    score_field = dict()
                    for cf in item.custom_fields:
                        if cf.name == self.score_field_name:
                            score_field = cf
                            break

                    try:
                        issue = Issue.objects.get(
                            redmine_id=item.id,
                            project_id=str(p.pk),
                        )

                        if issue.synchronized is False:
                            # Only the synchronized ones. The not synchronzied
                            # has priority from down up to server.
                            name = self.get_normalized_name(issue.subject, 20)
                            msg = f' - {name} (ID: {item.id}) - ignored'
                            self.stdout.write(self.style.SUCCESS(msg))
                            continue

                    except Issue.DoesNotExist:
                        issue = Issue(
                            redmine_id=item.id,
                            project_id=str(p.pk),
                        )
                        issue.synchronized = True

                    if score_field:
                        issue.score_field = score_field.value

                    issue.subject = item.subject
                    issue.tracker_id = str(tracker.pk)
                    issue.description = item.description

                    if hasattr(item, 'estimated_hours'):
                        issue.estimated_hours = item.estimated_hours

                    if version:
                        issue.target_version_id = str(version.pk)

                    issue.save()

                    name = self.get_normalized_name(item.subject, 20)
                    msg = f' - {name} (ID: {item.id})'
                    self.stdout.write(self.style.SUCCESS(msg))

            except ForbiddenError:

                self.stdout.write('Redmine issues: {}'.format(
                    self.style.SUCCESS('not supported')
                ))

            print('--------')

    def sync_out(self):
        print()
        self.stdout.write('Internal issues ...', ending='\r')

        qs = Issue.objects.filter(synchronized=False).order_by('created_at')
        num = qs.count()

        self.stdout.write(
            'Internal issues found: {}'.format(self.style.SUCCESS(
                num or '0'
            ))
        )
        print()

        try:
            score_card = CustomField.objects.get(name=SCORE_CARD_FIELD_NAME)
        except CustomField.DoesNotExist:
            score_card = None

        entities = dict()

        for i in qs:
            custom_fields = list()
            if score_card and i.score_field:
                custom_fields.append({
                    'id': score_card.redmine_id,
                    'value': i.score_field,
                })

            if i.redmine_id:
                redmine_instance = self.redmine.issue.get(i.redmine_id)
            else:
                redmine_instance = self.redmine.issue.new()

            redmine_instance.subject = i.subject
            redmine_instance.description = i.description
            redmine_instance.project_id = i.project.redmine_id
            redmine_instance.tracker = i.tracker.redmine_id
            redmine_instance.estimated_hours = i.estimated_hours

            if custom_fields:
                redmine_instance.custom_fields = custom_fields

            if i.target_version_id:
                redmine_instance.fixed_version_id = i.target_version.redmine_id

            redmine_instance.save()

            i.redmine_id = redmine_instance.id
            i.synchronized = True
            i.save()

            if i.entity_id:
                entities[i.entity_id] = i.entity

            name = self.get_normalized_name(i.subject, 20)
            msg = f' - {name} (ID: {i.redmine_id})'
            self.stdout.write(self.style.SUCCESS(msg))

        if entities:
            for _, entity in entities.items():
                entity.synchronized = True
                entity.save()
