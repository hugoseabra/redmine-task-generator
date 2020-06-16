"""
Base abstract class for planning class.
"""


class ScoreField:
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __iter__(self):
        data = {
            'id': self.id,
            'value': self.value,
        }

        for k, v in data.items():
            yield k, v


class TaskContentBuilder:
    def __init__(self,
                 name: str,
                 subject: str,
                 description: dict = None,
                 estimated_hours: int = None,
                 target_version_id: str = None,
                 score_field: ScoreField = None):

        self.name = name

        self.raw_subject = subject
        self.raw_description = description or dict()

        self.estimated_hours = estimated_hours
        self.target_version_id = target_version_id
        self.score_field = score_field

        self.holders = dict()
        self.holder_list = list()
        self.context_data = dict()

        self._collect_holders()

    @property
    def subject(self):
        subject_holders = self.holders.get('subject', [])

        data = dict()
        for holder in subject_holders:
            value = self.context_data.get(holder)
            if not value:
                continue
            data[holder] = value

        if not data:
            return self.raw_subject

        return self.raw_subject.format(**data)

    @property
    def description(self):
        desc_holders = self.holders.get('description', [])

        data = dict()
        for holder in desc_holders:
            value = self.context_data.get(holder)
            if not value:
                continue
            data[holder] = value

        if not data:
            return self.raw_description

        desc_items = list()

        for _, content in self.raw_description.items():
            if not data:
                desc_items.append(content)
                continue
            desc_items.append(content.format(**data))

        return '\n\n'.join(desc_items)

    def add_content(self, key, value):
        if key not in self.holder_list:
            raise Exception(f'{key} is not a valid key.')

        self.context_data[key] = value

    def _collect_holders(self):
        self.holders['subject'] = self._collect_holder_variables(
            content=self.raw_subject
        )

        desc_holders = list()
        for _, content in self.raw_description.items():
            desc_holders += self._collect_holder_variables(content=content)

        self.holders['description'] = list(set(desc_holders))

        for _, holders in self.holders.items():
            self.holder_list += holders

        self.holder_list = list(set(self.holder_list))

    @staticmethod
    def _collect_holder_variables(content: str):

        holders = list()
        collect = False
        holder = ''
        for _, i in enumerate(content):
            if i == '{':
                collect = True
                continue

            if i == '}':
                collect = False
                if holder:
                    holders.append(holder.strip())
                    holder = ''
                continue

            if collect is True:
                holder += i

        return list(set(holders))
