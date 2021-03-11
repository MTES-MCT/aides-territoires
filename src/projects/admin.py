from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.urls import reverse
from django.utils.safestring import mark_safe

from core.forms import RichTextField
from projects.models import Project
from categories.fields import CategoryMultipleChoiceField

from import_export.admin import ExportActionMixin
from import_export.formats import base_formats
from exporting.tasks import export_projects_as_csv, export_projects_as_xlsx


class ProjectForm(forms.ModelForm):
    description = RichTextField(label=_('Description'), required=False)

    categories = CategoryMultipleChoiceField(
        label=_('Categories'),
        required=False,
        widget=FilteredSelectMultiple(_('Categories'), True))

    class Meta:
        model = Project
        fields = '__all__'


class ProjectAdmin(ExportActionMixin, admin.ModelAdmin):

    form = ProjectForm
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    fields = [
        'name', 'slug', 'description', 'categories',
        'is_suggested', 'date_created', 'status'
    ]
    actions = [
        'export_csv', 'export_xlsx']
    formats = [base_formats.CSV, base_formats.XLSX]
    search_fields = ['name']
    list_filter = ['is_suggested', 'categories', 'status']
    readonly_fields = ['date_created']
    filter_vertical = ['categories']

    class Media:
        css = {'all': (
            'css/admin.css',
            '/static/trumbowyg/dist/ui/trumbowyg.css',
            )
        }
        js = [
            'admin/js/jquery.init.js',
            '/static/js/shared_config.js',
            '/static/js/plugins/softmaxlength.js',
            '/static/js/search/enable_softmaxlength.js',
            '/static/trumbowyg/dist/trumbowyg.js',
            '/static/trumbowyg/dist/langs/fr.js',
            '/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js',
            '/static/trumbowyg/dist/plugins/resizimg/resizable-resolveconflict.js',  # noqa
            '/static/jquery-resizable-dom/dist/jquery-resizable.js',
            '/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js',
            '/static/js/enable_rich_text_editor.js',
        ]

    def show_export_message(self, request):
        url = reverse('admin:exporting_dataexport_changelist')
        msg = _(
            f'Exported data will be available '
            f'<a href="{url}">here: {url}</a>')
        self.message_user(request, mark_safe(msg))

    def export_csv(self, request, queryset):
        projects_id_list = list(queryset.values_list('id', flat=True))
        export_projects_as_csv.delay(projects_id_list, request.user.id)
        self.show_export_message(request)
    export_csv.short_description = _(
        'Export selected projects as CSV in background task')

    def export_xlsx(self, request, queryset):
        projects_id_list = list(queryset.values_list('id', flat=True))
        export_projects_as_xlsx.delay(projects_id_list, request.user.id)
        self.show_export_message(request)
    export_xlsx.short_description = _(
        'Export selected projects as XLSX as background task')



admin.site.register(Project, ProjectAdmin)
