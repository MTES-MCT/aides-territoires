from django.contrib import admin

from categories.models import Theme, Category


class CategoryInline(admin.TabularInline):
    model = Category


class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name', 'short_description']
    search_fields = ['name']
    inlines = [CategoryInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'theme']
    fields = ['name', 'short_description', 'theme']
    autocomplete_fields = ['theme']


admin.site.register(Theme, ThemeAdmin)
admin.site.register(Category, CategoryAdmin)
