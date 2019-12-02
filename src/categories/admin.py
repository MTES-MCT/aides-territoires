from django.contrib import admin
from django.db import models

from categories.models import Theme, Category


class ShortTextareaMixin:
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(
            attrs={'rows': 3})},
    }


class CategoryInline(ShortTextareaMixin, admin.TabularInline):
    model = Category


class ThemeAdmin(ShortTextareaMixin, admin.ModelAdmin):
    list_display = ['name']
    fields = ['name', 'short_description']
    search_fields = ['name']
    inlines = [CategoryInline]


class CategoryAdmin(ShortTextareaMixin, admin.ModelAdmin):
    list_display = ['name', 'theme']
    fields = ['name', 'short_description', 'theme']
    search_fields = ['name', 'theme__name']
    autocomplete_fields = ['theme']


admin.site.register(Theme, ThemeAdmin)
admin.site.register(Category, CategoryAdmin)
