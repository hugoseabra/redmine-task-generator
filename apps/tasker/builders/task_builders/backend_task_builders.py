"""
Base abstract class for planning class.
"""

from .task_content_builders import TaskContentBuilder


class Field:
    def __init__(self, field_name, required=False, description: str = None):
        self.field_name = field_name
        self.required = required
        self.description = description

    def __iter__(self):
        data = {
            'field_name': self.field_name,
            'required': 'Sim' if self.required is True else 'Não',
            'description': self.description or '',
        }

        for k, v in data.items():
            yield k, v


class Endpoint:
    def __init__(self, method: str, uri: str, description: str = None):
        self.method = method.upper()
        self.uri = uri.lower()
        self.description = description

    def __iter__(self):
        data = {
            'method': self.method,
            'uri': self.uri,
            'description': self.description or '',
        }

        for k, v in data.items():
            yield k, v


class ModelContentBuilder(TaskContentBuilder):
    def __init__(self, field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_field = field
        self.fields = list()

    def add_field(self, field: Field):
        self.fields.append(field)

    def add_content(self, key, value):
        if key == 'fields':
            raise Exception('Key "fields" is reserved. Use method add_field()')

        return super().add_content(key, value)

    @property
    def description(self):
        self.context_data['fields'] = self._get_fields_content()
        return super().description

    def _get_fields_content(self):
        field_content = list()

        for f in self.fields:
            field_content.append(self.raw_field.format(**dict(f)))

        return '\n'.join(field_content)


class RestEndpointContentBuilder(TaskContentBuilder):
    def __init__(self, endpoint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_endpoint = endpoint
        self.endpoints = list()

    def add_endpoint(self, endpoint: Endpoint):
        self.endpoints.append(endpoint)

    def add_content(self, key, value):
        if key == 'endpoints':
            raise Exception('Key "endpoints" is reserved.'
                            ' Use method add_endpoint()')

        return super().add_content(key, value)

    @property
    def description(self):
        self.context_data['endpoints'] = self._get_endpoint_content()
        return super().description

    def _get_endpoint_content(self):
        content = list()

        for f in self.endpoints:
            content.append(self.raw_endpoint.format(**dict(f)))

        return '\n'.join(content)
