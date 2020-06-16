import json
import os

from django.conf import settings

from .task_builders.task_content_builders import TaskContentBuilder, ScoreField

CONF_FILE = os.path.join(settings.BASE_DIR, 'conf', 'ped.json')
CONF_CONTENT = json.load(open(CONF_FILE))


def get_research_task(research_name,
                      content=None,
                      estimated_hours: int = None,
                      target_version_id: str = None,
                      score_field: dict = None) -> TaskContentBuilder:
    data = CONF_CONTENT.get('research')

    if score_field:
        score_field = ScoreField(**score_field)

    task = TaskContentBuilder(
        name='[P&D] Research task',
        subject=data['subject'],
        description=data['description'],
        estimated_hours=estimated_hours,
        score_field=score_field,
        target_version_id=target_version_id,
    )

    task.add_content(key='research_name', value=research_name)
    if content:
        task.add_content(key='content', value=content)

    return task


def get_poc_task(lib_name,
                 content=None,
                 estimated_hours: int = None,
                 target_version_id: str = None,
                 score_field: dict = None) -> TaskContentBuilder:
    data = CONF_CONTENT.get('poc')

    if score_field:
        score_field = ScoreField(**score_field)

    task = TaskContentBuilder(
        name='[P&D] PoC task',
        subject=data['subject'],
        description=data['description'],
        score_field=score_field,
        estimated_hours=estimated_hours,
        target_version_id=target_version_id,
    )

    task.add_content(key='lib_name', value=lib_name)
    if content:
        task.add_content(key='content', value=content)

    return task
