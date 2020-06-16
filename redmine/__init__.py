from django.conf import settings
from redminelib import Redmine as DefaultRedmine

from .validator import RedmineInstanceValidator


class Redmine(DefaultRedmine):
    def __init__(self, url=None, key=None):
        url = url or settings.REDMINE_BASE_URL
        key = key or settings.REDMINE_API_KEY
        super().__init__(url=url, key=key)

        self.validator = RedmineInstanceValidator(client=self)

    @property
    def score_field(self):
        return self.validator.score_field

    def instance_errors(self):
        errors = list()
        if self.validator.track_errors:
            errors += self.validator.track_errors

        if self.validator.score_field_errors:
            errors += self.validator.score_field_errors

        return errors

    def instance_valid(self) -> bool:
        return self.validator.instance_valid()

    def project_valid(self, project_id) -> bool:
        return self.validator.project_valid(project_id)
