from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from core.models.mixins import UUIDPkMixin, DateTimeManagementMixin


class Tracker(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Tracker')
        verbose_name_plural = _('Trackers')
        ordering = ('name',)

    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        null=False,
        blank=False,
        unique=True,
    )
    redmine_id = models.IntegerField(
        verbose_name=_('Redmine ID'),
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'{self.name}'


class CustomField(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Custom field')
        verbose_name_plural = _('Custom fields')
        ordering = ('name',)

    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        null=False,
        blank=False,
    )
    redmine_id = models.IntegerField(
        verbose_name=_('Redmine ID'),
        null=False,
        blank=False,
    )
    possible_values = JSONField(
        verbose_name='possible values',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name}'
