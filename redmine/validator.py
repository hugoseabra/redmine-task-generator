from redmine.project_settings import PROJECT_DEFAULT_MODULES
from redmine.scores import SCORES, SCORE_CARD_FIELD_NAME
from redmine.trackers import TRACKERS


class RedmineInstanceValidator:
    """
    Instance validation for a given URL with provided configuration that
    this service is prepared to attend.

    The instamce needs to have the correct trackers and a custom field named
    'score' which is a list and must be the Score Card options.
    """

    def __init__(self, client):
        self.client = client

        self.score_field = None

        self.track_errors = list()
        self.score_field_errors = list()

        self.invalid_tracker_projects = list()
        self.invalid_module_projects = list()
        self.valid_projects = dict()

    def instance_valid(self):
        self._validate_trackers()
        self._validate_score_card_field()

        no_track_errors = len(self.track_errors) == 0
        no_score_field_errors = len(self.track_errors) == 0
        return no_track_errors is True and no_score_field_errors is True

    def project_valid(self, project_id):
        self._validate_projects()
        return project_id in self.valid_projects

    def get_score_card_values(self) -> list:
        values = list()
        for _, score in SCORES.items():
            values += [f'{k}. {v}' for k, v in score.items()]
        return values

    def _validate_trackers(self):
        trackers = self.client.tracker.all()
        tracker_names = [t.name for t in trackers]

        if len(tracker_names) > 0:

            for default_tracker in TRACKERS:
                if default_tracker not in tracker_names:
                    self.track_errors.append(
                        '"{}" was not found.'.format(default_tracker)
                    )
                    break
        else:
            self.track_errors.append('No tracker was found in the instance')

    def _validate_score_card_field(self):
        custom_fields = self.client.custom_field.all()

        field = None

        for c in custom_fields:
            if c.name == SCORE_CARD_FIELD_NAME:
                field = c
                break

        if not field:
            self.score_field_errors.append(
                'Score field with name "{}" was not found.'.format(
                    SCORE_CARD_FIELD_NAME
                )
            )
            return

        score_card_values = self.get_score_card_values()

        is_list = field.field_format == 'list'
        is_visible = field.visible is True
        is_issue = field.customized_type == 'issue'

        if is_list and is_visible and is_issue:
            if not field.possible_values:
                self.score_field_errors.append(
                    'Score field "{}" has no values in list.'.format(
                        field.id
                    )
                )
            else:
                for item in field.possible_values:
                    v = item.get('value')
                    if v and v not in score_card_values:
                        self.score_field_errors.append(
                            'Value not found in Score field "{}"'.format(
                                field.id
                            )
                        )

            if len(self.score_field_errors) == 0:
                self.score_field = field

        else:
            if is_list is False:
                self.score_field_errors.append(
                    'Score field "{}" is not a list format.'.format(
                        field.id
                    )
                )
            if is_visible is False:
                self.score_field_errors.append(
                    'Score field "{}" is not visible.'.format(
                        field.id
                    )
                )
            if is_issue is False:
                self.score_field_errors.append(
                    'Score field "{}" is not an issue field.'.format(
                        field.id
                    )
                )

    def _validate_projects(self):
        projects = self.client.project.all()

        for p in projects:
            tracker_names = [t.name for t in p.trackers]

            valid = True
            for t in TRACKERS:
                if t not in tracker_names:
                    self.invalid_tracker_projects.append(p)
                    valid = False

            module_names = p.enabled_modules
            for m in PROJECT_DEFAULT_MODULES:
                if m not in module_names:
                    self.invalid_module_projects.append(p)
                    valid = False

            if valid is True:
                self.valid_projects[p.id] = p
                self.valid_projects[p.identifier] = p
