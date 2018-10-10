from django.contrib import admin

from bundles.models import Bundle


class BundleAdmin(admin.ModelAdmin):
    """Admin module for bundles."""

    list_display = ['name', 'owner']
    autocomplete_fields = ['aids']


admin.site.register(Bundle, BundleAdmin)