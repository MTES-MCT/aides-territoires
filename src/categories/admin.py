from django.contrib import admin
from django.db import models

from categories.models import Theme, Category


class ShortTextareaMixin:
    formfield_overrides = {
        models.TextField: {
            "widget": admin.widgets.AdminTextareaWidget(attrs={"rows": 3})
        },
    }


class CategoryInline(ShortTextareaMixin, admin.TabularInline):
    model = Category
    ordering = ["name"]


class ThemeAdmin(ShortTextareaMixin, admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name", "slug", "short_description"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    inlines = [CategoryInline]
    ordering = ["name"]


class CategoryAdmin(ShortTextareaMixin, admin.ModelAdmin):
    list_display = ["name", "theme"]
    fields = ["name", "slug", "short_description", "theme"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "theme__name"]
    autocomplete_fields = ["theme"]
    ordering = ["theme__name", "name"]
    list_filter = ["theme"]


admin.site.register(Theme, ThemeAdmin)
admin.site.register(Category, CategoryAdmin)
