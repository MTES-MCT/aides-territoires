from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats

from core.forms import RichTextField
from projects.models import Project
from projects.resources import ProjectResource
from categories.fields import CategoryMultipleChoiceField


class ProjectForm(forms.ModelForm):
    description = RichTextField(label=_('Description'), required=False)

    categories = CategoryMultipleChoiceField(
        label=_('Categories'),
        required=False,
        widget=FilteredSelectMultiple(_('Categories'), True))

    class Meta:
        model = Project
        fields = '__all__'


class ProjectAdmin(ImportExportActionModelAdmin):

    resource_class = ProjectResource
    formats = [base_formats.CSV, base_formats.XLSX]
    form = ProjectForm
    list_display = ['name', 'status', 'date_created']
    prepopulated_fields = {'slug': ('name',)}
    fields = [
        'name', 'slug', 'description', 'categories',
        'key_words', 'is_suggested', 'date_created',
        'status'
    ]
    search_fields = ['name']
    list_filter = ['is_suggested', 'categories__theme', 'categories', 'status']
    readonly_fields = ['date_created']
    filter_vertical = ['categories']

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
