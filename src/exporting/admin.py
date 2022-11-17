from django.contrib import admin

from exporting.models import DataExport


class DataExportAdmin(admin.ModelAdmin):
    list_display = ["id", "exported_file", "author", "date_created"]
    search_fields = ["author__first_name", "author__last_name", "author__email"]
    list_filter = ["author"]
    raw_id_fields = ["author"]
    date_hierarchy = "date_created"


admin.site.register(DataExport, DataExportAdmin)
