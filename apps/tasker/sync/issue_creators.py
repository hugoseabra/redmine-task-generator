from django.db.transaction import atomic

from apps.redmine_project.models import Issue
from apps.redmine_settings.models import Tracker
from apps.tasker.builders.backend_helpers import (
    get_model_task,
    get_integrity_task,
    get_form_task,
    get_form_test_task,
    get_rest_serializer_task,
    get_rest_viewset_task,
    get_rest_endpoint_task,
)
from apps.tasker.models import Entity
from redmine.trackers import TRACKER_FUNCTIONALITY


class BackendIssueCreator:
    def __init__(self, entity: Entity):
        self.entity = entity

        self.tasks = list()
        self.tracker = Tracker.objects.get(name=TRACKER_FUNCTIONALITY)

    def create_tasks(self):
        score = None
        if self.entity.score:
            score = {
                'id': self.entity.score,
                'value': self.entity.get_form_score_display()
            }

        hours = self.entity.estimated_hours

        self.tasks.append(get_model_task(
            model=self.entity.model_alias,
            model_name=self.entity.model_name,
            fields=[
                {
                    'field_name': f.name,
                    'required': f.required,
                    'description': f.description
                }
                for f in self.entity.fields.all()
            ],
            pre_note=self.entity.pre_requisites,
            post_note=self.entity.important_notes,
            score_field=score,
            estimated_hours=float(hours) if hours else None,
            target_version_id=str(self.entity.target_version_id or ''),
        ))

        if self.entity.integrity_tests is True:
            score = None
            if self.entity.integrity_tests_score:
                score = {
                    'id': self.entity.integrity_tests_score,
                    'value': self.entity.get_integrity_tests_score_display()
                }

            hours = self.entity.integrity_tests_hours

            self.tasks.append(get_integrity_task(
                model=self.entity.model_alias,
                model_name=self.entity.model_name,
                content=self.entity.integrity_tests_desc,
                score_field=score,
                estimated_hours=float(hours) if hours else None,
                target_version_id=str(
                    self.entity.integrity_tests_version_id or ''
                ),
            ))

        if self.entity.form is True:
            score = None
            if self.entity.form_score:
                score = {
                    'id': self.entity.form_score,
                    'value': self.entity.get_form_score_display()
                }

            hours = self.entity.form_hours

            self.tasks.append(get_form_task(
                model=self.entity.model_alias,
                model_name=self.entity.model_name,
                content=self.entity.form_desc,
                score_field=score,
                estimated_hours=float(hours) if hours else None,
                target_version_id=str(self.entity.form_version_id or ''),
            ))

        if self.entity.form_tests is True:
            score = None
            if self.entity.form_tests_score:
                score = {
                    'id': self.entity.form_tests_score,
                    'value': self.entity.get_form_tests_score_display()
                }

            hours = self.entity.form_tests_hours

            self.tasks.append(get_form_test_task(
                model=self.entity.model_alias,
                model_name=self.entity.model_name,
                content=self.entity.form_tests_desc,
                score_field=score,
                estimated_hours=float(hours) if hours else None,
                target_version_id=str(self.entity.form_tests_version_id or ''),
            ))

        if self.entity.rest_serializer is True:
            score = None
            if self.entity.rest_serializer_score:
                score = {
                    'id': self.entity.rest_serializer_score,
                    'value': self.entity.get_rest_serializer_score_display()
                }

            hours = self.entity.rest_serializer_hours

            self.tasks.append(get_rest_serializer_task(
                model=self.entity.model_alias,
                model_name=self.entity.model_name,
                content=self.entity.rest_serializer_desc,
                score_field=score,
                estimated_hours=float(hours) if hours else None,
                target_version_id=str(
                    self.entity.rest_serializer_version_id or ''
                ),
            ))

        if self.entity.rest_viewset is True:
            score = None
            if self.entity.rest_viewset_score:
                score = {
                    'id': self.entity.rest_viewset_score,
                    'value': self.entity.get_rest_viewset_score_display(),
                }

            hours = self.entity.rest_viewset_hours

            self.tasks.append(get_rest_viewset_task(
                model=self.entity.model_alias,
                model_name=self.entity.model_name,
                content=self.entity.rest_viewset_desc,
                score_field=score,
                estimated_hours=float(hours) if hours else None,
                target_version_id=str(
                    self.entity.rest_viewset_version_id or ''
                ),
            ))

        ent = self.entity
        paths = list()

        if hasattr(ent, 'collection_endpoint') and ent.collection_endpoint:
            endpoint = self.entity.collection_endpoint
            paths.append({
                'method': 'GET',
                'uri': endpoint.path,
                'description': endpoint.description,
            })

            if endpoint.creation_endpoint is True:
                paths.append({
                    'method': 'POST',
                    'uri': endpoint.path,
                })

        if hasattr(ent, 'item_endpoint') and ent.item_endpoint:
            endpoint = self.entity.item_endpoint
            paths.append({
                'method': 'GET',
                'uri': endpoint.path,
                'description': endpoint.description,
            })

            if endpoint.edit_endpoint is True:
                paths.append({
                    'method': 'PATCH',
                    'uri': endpoint.path,
                })

            if endpoint.delete_endpoint is True:
                paths.append({
                    'method': 'DELETE',
                    'uri': endpoint.path,
                })

        for endpoint in self.entity.generic_endpoints.all():
            paths.append({
                'method': endpoint.method,
                'uri': endpoint.path,
                'description': endpoint.description,
            })

        score = None
        if self.entity.rest_endpoints_score:
            score = {
                'id': self.entity.rest_endpoints_score,
                'value': self.entity.get_rest_endpoints_score_display(),
            }

        hours = self.entity.rest_endpoints_hours

        self.tasks.append(get_rest_endpoint_task(
            model=self.entity.model_alias,
            model_name=self.entity.model_name,
            endpoints=paths,
            score_field=score,
            estimated_hours=float(hours) if hours else None,
            target_version_id=str(self.entity.rest_endpoints_version_id or ''),
        ))

    def create_issues(self):
        with atomic():
            for task in self.tasks:
                issue, _ = Issue.objects.get_or_create(
                    project_id=self.entity.project_id,
                    tracker=self.tracker,
                    subject=task.subject,
                )
                issue.score_field = task.score_field.value
                issue.description = task.description
                issue.estimated_hours = task.estimated_hours
                issue.synchronized = self.entity.synchronized
                issue.entity_id = str(self.entity.pk)
                issue.target_version_id = task.target_version_id
                issue.save()
