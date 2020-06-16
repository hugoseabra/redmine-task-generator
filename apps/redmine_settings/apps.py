from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RedmineSettingsConfig(AppConfig):
    name = 'apps.redmine_settings'
    label = 'redmine_settings'
    verbose_name = _('Redmine settings')
