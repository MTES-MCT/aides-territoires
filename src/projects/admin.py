from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats

from core.forms import RichTextField
from projects.models import Project
from projects.resources import ProjectResource


class ProjectForm(forms.ModelForm):
    description = RichTextField(label=_('Description'), required=False)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectAdmin(ImportExportActionModelAdmin):

    resource_class = ProjectResource
    formats = [base_formats.CSV, base_formats.XLSX]
    form = ProjectForm
    list_display = ['name', 'date_created']
    prepopulated_fields = {'slug': ('name',)}
    fields = [
        'name', 'slug', 'description',
        'key_words', 'beneficiary', 'aids_associated', 'due_date', 'date_created',
    ]
    search_fields = ['name']
    readonly_fields = ['date_created']
    autocomplete_fields = ['aids_associated', 'beneficiary']

    class Media:
        css = {
            'all': (
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


admin.site.register(Project, ProjectAdmin)
