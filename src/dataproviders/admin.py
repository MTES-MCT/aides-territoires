from django.contrib import admin

from dataproviders.models import DataSource


class DataSourceAdmin(admin.ModelAdmin):
    list_filter = ['contact_team']
    autocomplete_fields = ['backer', 'perimeter', 'contact_team']
    readonly_fields = ['date_created', 'date_updated', 'date_last_access']


admin.site.register(DataSource, DataSourceAdmin)
