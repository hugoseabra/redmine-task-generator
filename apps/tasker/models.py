import hashlib

from django.db import models
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _

from core.models.mixins import UUIDPkMixin, DateTimeManagementMixin
from redmine.scores import BACKEND_CHOICES, BACKEND_HOURS_CHOICES


class Entity(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Entity')
        verbose_name_plural = _('Entity')
        ordering = ('project__name', 'model_name', 'model_alias')

    project = models.ForeignKey(
        to='redmine_project.Project',
        verbose_name=_('Project'),
        on_delete=models.PROTECT,
        related_name='issues',
        null=False,
        blank=False,
    )
    model_name = models.CharField(
        verbose_name=_('model name'),
        max_length=100,
        null=False,
        blank=False,
    )
    model_alias = models.CharField(
        verbose_name=_('model alias'),
        max_length=100,
        null=False,
        blank=False,
    )
    pre_requisites = models.TextField(
        verbose_name=_('pre requisites'),
        null=True,
        blank=True,
    )
    important_notes = models.TextField(
        verbose_name=_('important notes'),
        null=True,
        blank=True,
    )
    score = models.CharField(
        verbose_name=_('Score'),
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
    target_version = models.ForeignKey(
        to='redmine_project.Version',
        on_delete=models.PROTECT,
        verbose_name=_('Target version'),
        related_name='models',
        null=True,
        blank=True,
    )

    integrity_tests = models.BooleanField(
        verbose_name=_('integrity tests'),
        default=False,
        null=False,
        blank=False,
    )
    integrity_tests_desc = models.TextField(
        verbose_name=_('integrity tsets description'),
        null=True,
        blank=True,
    )
    integrity_tests_score = models.CharField(
        verbose_name=_('Score for integrity tests'),
        choices=BACKEND_CHOICES,
        max_length=13,
        null=True,
        blank=True,
    )
    integrity_tests_hours = models.CharField(
        verbose_name=_('Estimated hours for integrity tests'),
        choices=BACKEND_HOURS_CHOICES,
        max_length=22,
        null=True,
        blank=True,
    )
    integrity_tests_version = models.ForeignKey(
        to='redmine_project.Version',
        on_delete=models.PROTECT,
        verbose_name=_('Integrity tests version'),
        related_name='integrity_tests',
        null=True,
        blank=True,
    )

    form = models.BooleanField(
        verbose_name=_('form'),
        default=False,
        null=False,
        blank=False,
    )
    form_desc = models.TextField(
        verbose_name=_('form description'),
        null=True,
        blank=True,
    )
    form_score = models.CharField(
        verbose_name=_('Score for form'),
        choices=BACKEND_CHOICES,
        max_length=13,
        null=True,
        blank=True,
    )
    form_hours = models.CharField(
        verbose_name=_('Estimated hours for form'),
        choices=BACKEND_HOURS_CHOICES,
        max_length=22,
        null=True,
        blank=True,
    )
    form_version = models.ForeignKey(
        to='redmine_project.Version',
        on_delete=models.PROTECT,
        verbose_name=_('Form version'),
        related_name='forms',
        null=True,
        blank=True,
    )

    form_tests = models.BooleanField(
        verbose_name=_('form tests'),
        default=False,
        null=False,
        blank=False,
    )
    form_tests_desc = models.TextField(
        verbose_name=_('form tests description'),
        null=True,
        blank=True,
    )
    form_tests_score = models.CharField(
        verbose_name=_('Score for form tests'),
        choices=BACKEND_CHOICES,
        max_length=13,
        null=True,
        blank=True,
    )
    form_tests_hours = models.CharField(
        verbose_name=_('Estimated hours for form tests'),
        choices=BACKEND_HOURS_CHOICES,
        max_length=22,
        null=True,
        blank=True,
    )
    form_tests_version = models.ForeignKey(
        to='redmine_project.Version',
        on_delete=models.PROTECT,
        verbose_name=_('Form tests version'),
        related_name='form_tests',
        null=True,
        blank=True,
    )

    rest_serializer = models.BooleanField(
        verbose_name=_('rest serializer'),
        default=False,
        null=False,
        blank=False,
    )
    rest_serializer_desc = models.TextField(
        verbose_name=_('rest serializer description'),
        null=True,
        blank=True,
    )
    rest_serializer_score = models.CharField(
        verbose_name=_('Score for serializer'),
        choices=BACKEND_CHOICES,
        max_length=13,
        null=True,
        blank=True,
    )
    rest_serializer_hours = models.CharField(
        verbose_name=_('Estimated hours for rest serializers'),
        choices=BACKEND_HOURS_CHOICES,
        max_length=22,
        null=True,
        blank=True,
    )
    rest_serializer_version = models.ForeignKey(
        to='redmine_project.Version',
        on_delete=models.PROTECT,
        verbose_name=_('Rest serializer version'),
        related_name='rest_serializers',
        null=True,
        blank=True,
    )

    rest_viewset = models.BooleanField(
        verbose_name=_('rest viewset'),
        default=False,
        null=False,
        blank=False,
    )
    rest_viewset_desc = models.TextField(
        verbose_name=_('rest viewset description'),
        null=True,
        blank=True,
    )
    rest_viewset_score = models.CharField(
        verbose_name=_('Score for viewset'),
        choices=BACKEND_CHOICES,
        max_length=13,
        null=True,
        blank=True,
    )
    rest_viewset_hours = models.CharField(
        verbose_name=_('Estimated hours for rest viewsets'),
        choices=BACKEND_HOURS_CHOICES,
        max_length=22,
        null=True,
        blank=True,
    )
    rest_viewset_version = models.ForeignKey(
        to='redmine_project.Version',
        on_delete=models.PROTECT,
        verbose_name=_('Rest viewset version'),
        related_name='rest_viewsets',
        null=True,
        blank=True,
    )

    rest_endpoints_score = models.CharField(
        verbose_name=_('Score for endpoints'),
        choices=BACKEND_CHOICES,
        max_length=13,
        null=True,
        blank=True,
    )
    rest_endpoints_hours = models.CharField(
        verbose_name=_('Estimated hours for rest endpoints'),
        choices=BACKEND_HOURS_CHOICES,
        max_length=22,
        null=True,
        blank=True,
    )
    rest_endpoints_version = models.ForeignKey(
        to='redmine_project.Version',
        on_delete=models.PROTECT,
        verbose_name=_('Rest endpoints version'),
        related_name='rest_endpoints',
        null=True,
        blank=True,
    )

    checksum = models.CharField(
        verbose_name=_('hash checksum'),
        max_length=32,
        null=False,
        blank=False,
        editable=False,
    )
    synchronized = models.BooleanField(
        verbose_name=_('synchronized'),
        default=False,
        null=False,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.model_alias

    def save(self, *args, **kwargs):
        checksum = self.get_hash_checksum()

        if self._state.adding is False:
            self.synchronized = checksum == self.checksum

        self.checksum = checksum

        super().save(*args, **kwargs)

    def get_hash_checksum(self):
        parts = [
            str(self.project_id),
            str(self.model_name),
            str(self.model_alias),
            str(self.score),
            str(self.estimated_hours),
            str(self.target_version_id),

            str(self.form),
            str(self.form_desc),
            str(self.form_score),
            str(self.form_hours),

            str(self.form_tests),
            str(self.form_tests_desc),
            str(self.form_tests_score),
            str(self.form_tests_hours),
            str(self.form_tests_version_id),

            str(self.integrity_tests),
            str(self.integrity_tests_desc),
            str(self.integrity_tests_score),
            str(self.integrity_tests_hours),
            str(self.integrity_tests_version_id),

            str(self.rest_serializer),
            str(self.rest_serializer_desc),
            str(self.rest_serializer_score),
            str(self.rest_serializer_hours),
            str(self.rest_serializer_version_id),

            str(self.rest_viewset),
            str(self.rest_viewset_desc),
            str(self.rest_viewset_score),
            str(self.rest_viewset_hours),
            str(self.rest_viewset_version_id),

            str(self.rest_endpoints_score),
            str(self.rest_endpoints_hours),
            str(self.rest_endpoints_version_id),
        ]

        for f in self.fields.all():
            parts += [
                str(f.name),
                str(f.description),
                str(f.required),
                str(f.order),
            ]

        if hasattr(self, 'collection_endpoint'):
            endpoint = self.collection_endpoint
            parts += [
                str(endpoint.path),
                str(endpoint.description),
                str(endpoint.creation_endpoint),
                str(endpoint.order),
            ]

        if hasattr(self, 'item_endpoint'):
            endpoint = self.item_endpoint
            parts += [
                str(endpoint.path),
                str(endpoint.description),
                str(endpoint.edit_endpoint),
                str(endpoint.delete_endpoint),
                str(endpoint.order),
            ]

        for endpoint in self.generic_endpoints.all():
            parts += [
                str(endpoint.path),
                str(endpoint.description),
                str(endpoint.method),
            ]

        content = ';;;'.join(parts)
        return hashlib.md5(content.encode()).hexdigest()


class OrderableManager(models.Manager):

    def next_order(self, entity):
        counter = self.filter(entity_id=entity.pk).aggregate(max=Max('order'))
        if counter['max']:
            return counter['max'] + 1

        return 1


class EntityField(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Entity field')
        verbose_name_plural = _('Entity fields')
        unique_together = (('entity', 'name',),)
        ordering = ('order',)

    objects = OrderableManager()

    entity = models.ForeignKey(
        to='tasker.Entity',
        verbose_name=_('Entity'),
        on_delete=models.PROTECT,
        related_name='fields',
        null=False,
        blank=False,
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_('important notes'),
        null=True,
        blank=True,
    )
    required = models.BooleanField(
        verbose_name=_('required'),
        default=False,
        null=False,
        blank=False,
    )
    order = models.SmallIntegerField(
        verbose_name=_('order'),
        null=False,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = EntityField.objects.next_order(entity=self.entity)

        super().save(*args, **kwargs)


class CollectionEndpoint(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Collection Endpoint')
        verbose_name_plural = _('Collection Endpoint')

    objects = OrderableManager()

    entity = models.OneToOneField(
        to='tasker.Entity',
        verbose_name=_('Entity'),
        on_delete=models.PROTECT,
        related_name='collection_endpoint',
        null=False,
        blank=False,
    )
    path = models.CharField(
        verbose_name=_('path'),
        max_length=100,
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_('important notes'),
        null=True,
        blank=True,
    )
    creation_endpoint = models.BooleanField(
        verbose_name=_('Creaton endpoint enabled'),
        default=False,
        null=False,
        blank=False,
    )

    order = models.SmallIntegerField(
        verbose_name=_('order'),
        null=False,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = EntityField.objects.next_order(entity=self.entity)

        super().save(*args, **kwargs)


class ItemEndpoint(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Item Endpoint')
        verbose_name_plural = _('Item Endpoint')

    objects = OrderableManager()

    entity = models.OneToOneField(
        to='tasker.Entity',
        verbose_name=_('Entity'),
        on_delete=models.PROTECT,
        related_name='item_endpoint',
        null=False,
        blank=False,
    )
    path = models.CharField(
        verbose_name=_('path'),
        max_length=100,
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_('important notes'),
        null=True,
        blank=True,
    )
    edit_endpoint = models.BooleanField(
        verbose_name=_('POST/PATCH endpoint included'),
        default=False,
        null=False,
        blank=False,
    )
    delete_endpoint = models.BooleanField(
        verbose_name=_('DELETE endpoint included'),
        default=False,
        null=False,
        blank=False,
    )
    order = models.SmallIntegerField(
        verbose_name=_('order'),
        null=False,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = EntityField.objects.next_order(entity=self.entity)

        super().save(*args, **kwargs)


class GenericEndpoint(UUIDPkMixin, DateTimeManagementMixin):
    class Meta:
        verbose_name = _('Generic Endpoint')
        verbose_name_plural = _('Generic Endpoint')

    objects = OrderableManager()

    entity = models.ForeignKey(
        to='tasker.Entity',
        verbose_name=_('Entity'),
        on_delete=models.PROTECT,
        related_name='generic_endpoints',
        null=False,
        blank=False,
    )
    method = models.CharField(
        verbose_name=_('Method'),
        choices=(
            ('GET', 'GET',),
            ('POST', 'POST',),
            ('PUT', 'PUT',),
            ('PATCH', 'PATCH',),
            ('DELETE', 'DELETE',),
        ),
        max_length=6,
        null=False,
        blank=False,
    )
    path = models.CharField(
        verbose_name=_('path'),
        max_length=100,
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_('important notes'),
        null=True,
        blank=True,
    )
    order = models.SmallIntegerField(
        verbose_name=_('order'),
        null=False,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = EntityField.objects.next_order(entity=self.entity)

        super().save(*args, **kwargs)
