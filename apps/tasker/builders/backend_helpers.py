import json
import os

from django.conf import settings

from .task_builders.backend_task_builders import (
    Endpoint,
    Field,
    ModelContentBuilder,
    RestEndpointContentBuilder,
)
from .task_builders.task_content_builders import ScoreField
from .task_builders.task_content_builders import TaskContentBuilder

CONF_FILE = os.path.join(settings.BASE_DIR, 'conf', 'backend.json')
CONF_CONTENT = json.load(open(CONF_FILE))


def get_model_task(model,
                   model_name,
                   fields: list,
                   score_field: dict = None,
                   estimated_hours: int = None,
                   target_version_id: str = None,
                   pre_note=None,
                   post_note=None) -> ModelContentBuilder:
    data = CONF_CONTENT.get('model')

    if score_field:
        score_field = ScoreField(**score_field)

    task = ModelContentBuilder(
        name='[Backend] Model task',
        field=data['field'],
        subject=data['subject'],
        description=data['description'],
        score_field=score_field,
        estimated_hours=estimated_hours,
        target_version_id=target_version_id,
    )

    task.add_content(key='model', value=model)
    task.add_content(key='model_name', value=model_name)
    if pre_note:
        task.add_content(key='pre_note', value=pre_note)

    if fields:
        for f in fields:
            task.add_field(Field(**f))

    if post_note:
        task.add_content(key='post_note', value=post_note)

    return task


def get_integrity_task(model,
                       model_name,
                       content=None,
                       estimated_hours: int = None,
                       target_version_id: str = None,
                       score_field: dict = None) -> TaskContentBuilder:
    if score_field:
        score_field = ScoreField(**score_field)

    data = CONF_CONTENT.get('integrity_test')

    task = TaskContentBuilder(
        name='[Backend] Integrity test task',
        subject=data['subject'],
        description=data['description'],
        estimated_hours=estimated_hours,
        score_field=score_field,
        target_version_id=target_version_id,
    )

    task.add_content(key='model', value=model)
    task.add_content(key='model_name', value=model_name)

    if content:
        task.add_content(key='content', value=content)

    return task


def get_form_task(model,
                  model_name,
                  content=None,
                  estimated_hours: int = None,
                  target_version_id: str = None,
                  score_field: dict = None) -> TaskContentBuilder:
    if score_field:
        score_field = ScoreField(**score_field)

    data = CONF_CONTENT.get('form')

    task = TaskContentBuilder(
        name='[Backend] Form task',
        subject=data['subject'],
        description=data['description'],
        estimated_hours=estimated_hours,
        score_field=score_field,
        target_version_id=target_version_id,
    )

    task.add_content(key='model', value=model)
    task.add_content(key='model_name', value=model_name)

    if content:
        task.add_content(key='content', value=content)

    return task


def get_form_test_task(model,
                       model_name,
                       content=None,
                       estimated_hours: int = None,
                       target_version_id: str = None,
                       score_field: dict = None) -> TaskContentBuilder:
    data = CONF_CONTENT.get('form_test')

    if score_field:
        score_field = ScoreField(**score_field)

    task = TaskContentBuilder(
        name='[Backend] Form test task',
        subject=data['subject'],
        description=data['description'],
        estimated_hours=estimated_hours,
        score_field=score_field,
        target_version_id=target_version_id,
    )

    task.add_content(key='model', value=model)
    task.add_content(key='model_name', value=model_name)

    if content:
        task.add_content(key='content', value=content)

    return task


def get_rest_serializer_task(model,
                             model_name,
                             content=None,
                             estimated_hours: int = None,
                             target_version_id: str = None,
                             score_field: dict = None) -> TaskContentBuilder:
    data = CONF_CONTENT.get('rest_serializer')

    if score_field:
        score_field = ScoreField(**score_field)

    task = TaskContentBuilder(
        name='[Backend] Rest serializer task',
        subject=data['subject'],
        description=data['description'],
        score_field=score_field,
        estimated_hours=estimated_hours,
        target_version_id=target_version_id,
    )

    task.add_content(key='model', value=model)
    task.add_content(key='model_name', value=model_name)

    if content:
        task.add_content(key='content', value=content)

    return task


def get_rest_viewset_task(model,
                          model_name,
                          content=None,
                          estimated_hours: int = None,
                          target_version_id: str = None,
                          score_field: dict = None) -> TaskContentBuilder:
    data = CONF_CONTENT.get('rest_viewset')

    if score_field:
        score_field = ScoreField(**score_field)

    task = TaskContentBuilder(
        name='[Backend] Rest viewset task',
        subject=data['subject'],
        description=data['description'],
        score_field=score_field,
        estimated_hours=estimated_hours,
        target_version_id=target_version_id,
    )

    task.add_content(key='model', value=model)
    task.add_content(key='model_name', value=model_name)

    if content:
        task.add_content(key='content', value=content)

    return task


def get_rest_endpoint_task(
        model,
        model_name,
        endpoints: list,
        estimated_hours: int = None,
        target_version_id: str = None,
        score_field: dict = None) -> RestEndpointContentBuilder:
    data = CONF_CONTENT.get('rest_endpoints')

    if score_field:
        score_field = ScoreField(**score_field)

    task = RestEndpointContentBuilder(
        name='[Backend] Rest endpoint task',
        endpoint=data['endpoint'],
        subject=data['subject'],
        description=data['description'],
        score_field=score_field,
        estimated_hours=estimated_hours,
        target_version_id=target_version_id,
    )

    task.add_content(key='model', value=model)
    task.add_content(key='model_name', value=model_name)

    if endpoints:
        for e in endpoints:
            task.add_endpoint(Endpoint(**e))

    return task
