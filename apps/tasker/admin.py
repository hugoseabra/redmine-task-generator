# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from . import models
from apps.redmine_project import models as project_models


class FieldInline(admin.StackedInline):
    model = models.EntityField
    extra = 0
    readonly_fields = ('order',)


class CollectionEndpointInline(admin.StackedInline):
    model = models.CollectionEndpoint
    extra = 0
    max_num = 1


class ItemEndpointInline(admin.StackedInline):
    model = models.ItemEndpoint
    extra = 0
    max_num = 1


class GenericEndpointInline(admin.StackedInline):
    model = models.GenericEndpoint
    extra = 0


@admin.register(models.Entity)
class EntityAdmin(admin.ModelAdmin):
    inlines = (
        FieldInline,
        CollectionEndpointInline,
        ItemEndpointInline,
        GenericEndpointInline,
    )
    list_display = (
        'get_model',
        'project',
        'integrity_tests',
        'form',
        'form_tests',
        'rest_serializer',
        'rest_viewset',
        'synchronized',
    )
    readonly_fields = ('pk', 'synchronized', 'checksum',)
    list_filter = (
        'created_at',
        'updated_at',
        'integrity_tests',
        'form',
        'form_tests',
        'rest_serializer',
        'rest_viewset',
        'synchronized',
    )
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Model', {
            'fields': (
                'pk',
                'synchronized',
                'checksum',
                'project',
                'model_alias',
                'model_name',
                'pre_requisites',
                'important_notes',
                'score',
                'estimated_hours',
                'target_version',
            ),
        }),
        ('Integrity Tests', {
            'fields': (
                'integrity_tests',
                'integrity_tests_desc',
                'integrity_tests_score',
                'integrity_tests_hours',
                'integrity_tests_version',
            ),
        }),
        ('Form', {
            'fields': (
                'form',
                'form_desc',
                'form_score',
                'form_hours',
                'form_version',
            ),
        }),
        ('Form tests', {
            'fields': (
                'form_tests',
                'form_tests_desc',
                'form_tests_score',
                'form_tests_hours',
                'form_tests_version',
            ),
        }),
        ('REST Serializer', {
            'fields': (
                'rest_serializer',
                'rest_serializer_desc',
                'rest_serializer_score',
                'rest_serializer_hours',
                'rest_serializer_version',
            ),
        }),
        ('REST Viewset', {
            'fields': (
                'rest_viewset',
                'rest_viewset_desc',
                'rest_viewset_score',
                'rest_viewset_hours',
                'rest_viewset_version',
            ),
        }),
        ('REST Endpoints', {
            'fields': (
                'rest_endpoints_score',
                'rest_endpoints_hours',
                'rest_endpoints_version',
            ),
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_project_id = None

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.project_id:
            self.current_project_id = obj.project_id
        else:
            self.current_project_id = None

        return super().get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if self.current_project_id:
            if db_field.name == "target_version":
                kwargs["queryset"] = project_models.Version.objects.filter(
                    project_id=self.current_project_id,
                )

            if db_field.name == "integrity_tests_version":
                kwargs["queryset"] = project_models.Version.objects.filter(
                    project_id=self.current_project_id,
                )

            if db_field.name == "form_version":
                kwargs["queryset"] = project_models.Version.objects.filter(
                    project_id=self.current_project_id,
                )

            if db_field.name == "form_tests_version":
                kwargs["queryset"] = project_models.Version.objects.filter(
                    project_id=self.current_project_id,
                )

            if db_field.name == "rest_serializer_version":
                kwargs["queryset"] = project_models.Version.objects.filter(
                    project_id=self.current_project_id,
                )

            if db_field.name == "rest_viewset_version":
                kwargs["queryset"] = project_models.Version.objects.filter(
                    project_id=self.current_project_id,
                )

            if db_field.name == "rest_endpoints_version":
                kwargs["queryset"] = project_models.Version.objects.filter(
                    project_id=self.current_project_id,
                )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_model(self, instance):
        return format_html(
            f'{instance.model_name} (<small>{instance.model_alias}</small>)'
        )

    get_model.short_description = _('model')
