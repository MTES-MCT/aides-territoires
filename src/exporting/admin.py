from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ExportActionMixin
from import_export.formats import base_formats

from exporting.models import DataExport
from exporting import tasks as exporting_tasks



class DataExportAdmin(admin.ModelAdmin):
    list_display = ['id', 'exported_file', 'author', 'date_created']
    search_fields = [
        'author__first_name', 'author__last_name', 'author__email']
    list_filter = ['author']
    raw_id_fields = ['author']
    date_hierarchy = 'date_created'


class AidExportMixin(ExportActionMixin):
    formats = [base_formats.CSV, base_formats.XLSX]
    actions = [
        'export_admin_action',
        'export_csv', 'export_xlsx',
    ]

    def export_csv(self, request, queryset):
        aids_id_list = list(queryset.values_list('id', flat=True))
        exporting_tasks.export_aids_as_csv.delay(aids_id_list, request.user.id)
        self.show_export_message(request)
    export_csv.short_description = _(
        'Export selected Aids as CSV in background task')

    def export_xlsx(self, request, queryset):
        aids_id_list = list(queryset.values_list('id', flat=True))
        exporting_tasks.export_aids_as_xlsx.delay(aids_id_list, request.user.id)
        self.show_export_message(request)
    export_xlsx.short_description = _(
        'Export selected Aids as XLSX as background task')

    def export_admin_action(self, request, queryset):
        # We do a noop override of this method, just because
        # we want to customize it's short description
        return super().export_admin_action(request, queryset)
    export_admin_action.short_description = _(
        'Export and download selected Aids')


admin.site.register(DataExport, DataExportAdmin)
