from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models.mixins import UUIDPkMixin, DateTimeManagementMixin
from redmine.scores import BACKEND_CHOICES, BACKEND_HOURS_CHOICES


class Project(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ('name',)

    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        null=False,
        blank=False,
    )
    redmine_id = models.CharField(
        verbose_name=_('Redmine ID'),
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name}'


class Category(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Issue category')
        verbose_name_plural = _('Issue categories')
        ordering = ('project__name', 'name',)

    project = models.ForeignKey(
        to='redmine_project.Project',
        verbose_name=_('Project'),
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )

    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        null=False,
        blank=False,
        unique=True,
    )
    redmine_id = models.IntegerField(
        verbose_name=_('Redmine ID'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name}'


class Version(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Version')
        verbose_name_plural = _('Versions')
        ordering = ('project__name', 'due_date', 'name',)

    project = models.ForeignKey(
        to='redmine_project.Project',
        verbose_name=_('Project'),
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )

    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        null=False,
        blank=False,
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=20,
        null=True,
        blank=True,
    )
    due_date = models.DateField(
        verbose_name=_('due date'),
        max_length=100,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_('description'),
        null=True,
        blank=True,
    )
    redmine_id = models.IntegerField(
        verbose_name=_('Redmine ID'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name}'


class Issue(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Issue')
        verbose_name_plural = _('Issues')
        ordering = ('project__name', 'subject',)

    project = models.ForeignKey(
        to='redmine_project.Project',
        verbose_name=_('Project'),
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    tracker = models.ForeignKey(
        to='redmine_settings.Tracker',
        verbose_name=_('tracker'),
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    target_version = models.ForeignKey(
        to='redmine_project.Version',
        verbose_name=_('target version'),
        on_delete=models.PROTECT,
        related_name='issues',
        null=True,
        blank=True,
    )
    subject = models.CharField(
        verbose_name=_('subject'),
        max_length=100,
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_('description'),
        null=True,
        blank=True,
    )
    score_field = models.CharField(
        verbose_name=_('Score field'),
        choices=BACKEND_CHOICES,
        max_length=13,
        null=True,
        blank=True,
    )
    estimated_hours = models.CharField(
        verbose_name=_('Estimated hours'),
        choices=BACKEND_HOURS_CHOICES,
        max_length=22,
        null=True,
        blank=True,
    )
    redmine_id = models.IntegerField(
        verbose_name=_('Redmine ID'),
        null=True,
        blank=True,
    )
    synchronized = models.BooleanField(
        verbose_name=_('synchronized'),
        default=False,
        null=False,
        blank=True,
        editable=False,
    )
    entity = models.ForeignKey(
        to='tasker.Entity',
        verbose_name=_('entity'),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.subject}'
