import json
import os

from django.conf import settings

from .task_builders.task_content_builders import TaskContentBuilder, ScoreField

CONF_FILE = os.path.join(settings.BASE_DIR, 'conf', 'ped.json')
CONF_CONTENT = json.load(open(CONF_FILE))


def get_implementation_task(lib_name,
                            pre_note=None,
                            content=None,
                            post_note=None,
                            estimated_hours: int = None,
                            target_version_id: str = None,
                            score_field: dict = None) -> TaskContentBuilder:
    data = CONF_CONTENT.get('implementation')

    if score_field:
        score_field = ScoreField(**score_field)

    task = TaskContentBuilder(
        name='[LIB] Implementation task',
        subject=data['subject'],
        description=data['description'],
        score_field=score_field,
        estimated_hours=estimated_hours,
        target_version_id=target_version_id,
    )

    task.add_content(key='lib_name', value=lib_name)
    if pre_note:
        task.add_content(key='pre_note', value=pre_note)

    if content:
        task.add_content(key='content', value=content)

    if post_note:
        task.add_content(key='post_note', value=post_note)

    return task


def get_thirdy_party_task(lib_name,
                          pre_note=None,
                          content=None,
                          post_note=None,
                          estimated_hours: int = None,
                          target_version_id: str = None,
                          score_field: dict = None) -> TaskContentBuilder:
    data = CONF_CONTENT.get('implementation')

    if score_field:
        score_field = ScoreField(**score_field)

    task = TaskContentBuilder(
        name='[LIB] Third party task',
        subject=data['subject'],
        description=data['description'],
        score_field=score_field,
        estimated_hours=estimated_hours,
        target_version_id=target_version_id,
    )

    task.add_content(key='lib_name', value=lib_name)

    if pre_note:
        task.add_content(key='pre_note', value=pre_note)

    if content:
        task.add_content(key='content', value=content)

    if post_note:
        task.add_content(key='post_note', value=post_note)

    return task
