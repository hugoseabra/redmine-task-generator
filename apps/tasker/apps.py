from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TaskerConfig(AppConfig):
    name = 'apps.tasker'
    label = 'tasker'
    verbose_name = _('Tasker')
