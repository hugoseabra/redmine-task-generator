# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'get_name',
        'redmine_id',
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}
    date_hierarchy = 'created_at'

    def get_name(self, instance):
        return format_html(
            f'{instance.name} (<small>{instance.slug}</small>)'
        )

    get_name.short_description = _('name')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'project',
        'redmine_id',
    )
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('name', 'project__name')
    date_hierarchy = 'created_at'


@admin.register(models.Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'due_date',
        'project',
        'status',
        'redmine_id',
    )
    list_filter = ('created_at', 'updated_at', 'due_date')
    search_fields = ('name', 'project__name',)
    date_hierarchy = 'created_at'


@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'project',
        'tracker',
        'score_field',
        'redmine_id',
        'synchronized',
    )
    readonly_fields = ('synchronized',)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('subject', 'tracker__name', 'project__name',)
    date_hierarchy = 'created_at'
