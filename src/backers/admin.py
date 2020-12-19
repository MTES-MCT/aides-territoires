from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from import_export import resources
from import_export.admin import ImportMixin
from import_export.formats import base_formats

from core.forms import RichTextField
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS

from backers.models import Backer


class BackerForm(forms.ModelForm):
    description = RichTextField(label=_('Description'))

    class Meta:
        model = Backer
        fields = '__all__'


class BackerResource(resources.ModelResource):
    """Resource for Import-export."""

    class Meta:
        model = Backer
        skip_unchanged = True
        # name must be unique
        import_id_fields = ('name',)
        fields = ('name',)


class BackerAdmin(ImportMixin, admin.ModelAdmin):
    """Admin module for aid backers."""

    resource_class = BackerResource
    form = BackerForm
    formats = [base_formats.CSV, base_formats.XLSX]
    list_display = ['name', 'slug', 'is_corporate', 'nb_financed_aids',
                    'nb_instructed_aids', 'is_spotlighted']
    search_fields = ['name']
    ordering = ['name']
    filter_fields = ['is_corporate']
    list_editable = ['is_corporate', 'is_spotlighted']
    list_filter = ['is_corporate', 'is_spotlighted']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['display_related_aids']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs \
            .annotate_aids_count(Backer.financed_aids, 'nb_financed_aids') \
            .annotate_aids_count(Backer.instructed_aids, 'nb_instructed_aids')
        return qs

    def nb_financed_aids(self, obj):
        return obj.nb_financed_aids
    nb_financed_aids.short_description = _('Financed aids')
    nb_financed_aids.admin_order_field = 'nb_financed_aids'

    def nb_instructed_aids(self, obj):
        return obj.nb_instructed_aids
    nb_instructed_aids.short_description = _('Instructed aids')
    nb_instructed_aids.admin_order_field = 'nb_instructed_aids'

    def display_related_aids(self, obj):
        related_aid_html = format_html('<ul>')
        for aid in obj.financed_aids.all().order_by('name'):
            url = reverse("admin:aids_aid_change", args=(aid.pk,))
            related_aid_html += format_html(
                '<li><a href="{url}">{name} (ID : {id})</a></li>',
                url=url,
                name=aid.name,
                id=aid.pk
            )
        related_aid_html += format_html('</ul>')
        return related_aid_html
    display_related_aids.short_description = _('Related aids')

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
            '/static/js/plugins/softmaxlength.js',
            '/static/js/search/enable_softmaxlength.js',
            '/static/trumbowyg/dist/trumbowyg.js',
            '/static/trumbowyg/dist/langs/fr.js',
            '/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js',
            '/static/trumbowyg/dist/plugins/resizimg/resizable-resolveconflict.js',  # noqa
            '/static/jquery-resizable-dom/dist/jquery-resizable.js',
            '/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js',
            '/static/js/enable_rich_text_editor.js',
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS


admin.site.register(Backer, BackerAdmin)
