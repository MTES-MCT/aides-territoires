from django import forms
from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

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
    list_display = ['name', 'slug', 'nb_aids', 'date_created']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['date_created']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('aids') \
               .annotate(aid_count=Count('aids'))
        return qs

    def nb_aids(self, obj):
        return obj.aid_count
    nb_aids.short_description = "Nombre d'aides"
    nb_aids.admin_order_field = 'aid_count'


admin.site.register(Program, ProgramAdmin)
