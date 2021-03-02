from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from core.forms import RichTextField
from programs.models import Program
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class ProgramAdminForm(forms.ModelForm):
    description = RichTextField(
        label=_('Description'))


class ProgramAdmin(admin.ModelAdmin):

    class Media:
        css = {
            'all': (
                '/static/css/admin.css',
                '/static/trumbowyg/dist/ui/trumbowyg.css',
            )
        }
        js = [
            'admin/js/jquery.init.js',
            '/static/js/shared_config.js',
            '/static/trumbowyg/dist/trumbowyg.js',
            '/static/trumbowyg/dist/langs/fr.js',
            '/static/js/enable_rich_text_editor.js',
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS

    form = ProgramAdminForm
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    fields = [
        'name', 'slug', 'logo', 'short_description', 'description'
    ]
    search_fields = ['name']


admin.site.register(Program, ProgramAdmin)
