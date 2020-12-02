from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from import_export import resources
from import_export.admin import ImportMixin
from import_export.formats import base_formats

from backers.models import Backer


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
    formats = [base_formats.CSV, base_formats.XLSX]
    list_display = ['name', 'slug', 'is_corporate', 'nb_financed_aids',
                    'nb_instructed_aids', 'is_spotlighted']
    search_fields = ['name']
    ordering = ['name']
    filter_fields = ['is_corporate']
    list_editable = ['is_corporate']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs \
            .annotate_aids_count(Backer.financed_aids, 'nb_financed_aids') \
            .annotate_aids_count(Backer.instructed_aids, 'nb_instructed_aids')
        return qs

    def get_readonly_fields(self, request, obj=None):
        fields = ['display_related_aids']
        # When we are on editing mode, we want the slug field to be
        # readonly. When obj is there, is means we are on editing mode.
        if obj:
            fields.append('slug')
        return fields

    def get_prepopulated_fields(self, request, obj=None):
        fields = {}
        # When we are ading a new object, we want the slug field to be
        # prepopulated. Note that prepopulated fields cannot be set as
        # readonly. When obj is not there, it means we are adding a new
        # instance.
        if not obj:
            fields.update({'slug': ('name',)})
        return fields

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


admin.site.register(Backer, BackerAdmin)
