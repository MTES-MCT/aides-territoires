from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.forms import RichTextField
from projects.models import Project


class ProjectForm(forms.ModelForm):
    description = RichTextField(label=_('Description'), required=False)

    class Meta:
        model = Project
        fields = '__all__'

class ProjectAdmin(admin.ModelAdmin):

    form = ProjectForm
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    fields = [
        'name', 'slug', 'description', 'categories',
        'is_suggested', 'date_created'
    ]
    search_fields = ['name']
    list_filter = ['is_suggested', 'categories']
    readonly_fields = ['date_created']

    class Media:
        css = {'all': ('css/admin.css',)}
        js = [
            '/static/js/enable_rich_text_editor.js',
        ]


admin.site.register(Project, ProjectAdmin)