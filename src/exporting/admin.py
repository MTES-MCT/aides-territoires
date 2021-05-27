from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ExportActionMixin
from import_export.formats import base_formats

from core.admin_actions import ExtendedActionsMixin
from exporting import tasks as exporting_tasks
from exporting.models import DataExport


class DataExportAdmin(admin.ModelAdmin):
    list_display = ['id', 'exported_file', 'author', 'date_created']
    search_fields = [
        'author__first_name', 'author__last_name', 'author__email']
    list_filter = ['author']
    raw_id_fields = ['author']
    date_hierarchy = 'date_created'


class AidExportMixin(ExtendedActionsMixin, ExportActionMixin):
    EXPORT_SELECTED_AIDS = [
        'export_admin_action',
        'export_csv', 'export_xlsx',
    ]
    EXPORT_ALL_AIDS = [
        'export_published_aids_csv', 'export_published_aids_xlsx',
        'export_live_aids_csv', 'export_live_aids_xlsx'
    ]

    formats = [base_formats.CSV, base_formats.XLSX]
    actions = EXPORT_SELECTED_AIDS + EXPORT_ALL_AIDS
    extended_actions = EXPORT_ALL_AIDS

    def export_csv(self, request, queryset):
        aids_id_list = list(queryset.values_list('id', flat=True))
        exporting_tasks.export_aids_as_csv.delay(aids_id_list, request.user.id)
        self.show_export_message(request)
    export_csv.short_description = _(
        'Export selected Aids as CSV in background task')

    def export_xlsx(self, request, queryset):
        aids_id_list = list(queryset.values_list('id', flat=True))
        exporting_tasks.export_aids_as_xlsx.delay(
            aids_id_list, request.user.id)
        self.show_export_message(request)
    export_xlsx.short_description = _(
        'Export selected Aids as XLSX as background task')

    def export_published_aids_csv(self, request, queryset):
        exporting_tasks.export_published_aids_as_csv.delay(request.user.id)
        self.show_export_message(request)
    export_published_aids_csv.short_description = (
        'Exporter toutes les aides publiées en CSV')

    def export_published_aids_xlsx(self, request, queryset):
        exporting_tasks.export_published_aids_as_xlsx.delay(request.user.id)
        self.show_export_message(request)
    export_published_aids_xlsx.short_description = (
        'Exporter toutes les aides publiées en XLSX')

    def export_live_aids_csv(self, request, queryset):
        exporting_tasks.export_live_aids_as_csv.delay(request.user.id)
        self.show_export_message(request)
    export_live_aids_csv.short_description = (
        'Exporter toutes les aides affichées en CSV')

    def export_live_aids_xlsx(self, request, queryset):
        exporting_tasks.export_live_aids_as_xlsx.delay(request.user.id)
        self.show_export_message(request)
    export_live_aids_xlsx.short_description = (
        'Exporter toutes les aides affichées en XLSX')

    def export_admin_action(self, request, queryset):
        # We do a noop override of this method, just because
        # we want to customize it's short description
        return super().export_admin_action(request, queryset)
    export_admin_action.short_description = _(
        'Export and download selected Aids')


admin.site.register(DataExport, DataExportAdmin)
