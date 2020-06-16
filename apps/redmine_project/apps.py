from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RedmineProjectConfig(AppConfig):
    name = 'redmine_project'
    verbose_name = _('Redmine project')
