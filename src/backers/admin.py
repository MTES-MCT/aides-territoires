from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe
from django.utils.translation import ugettext_lazy as _



from backers.models import Backer


class BackerAdmin(admin.ModelAdmin):
    """Admin module for aid backers."""

    list_display = ['name', 'is_corporate', 'nb_financed_aids',
                    'nb_instructed_aids']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    filter_fields = ['is_corporate']
    list_editable = ['is_corporate']
    readonly_fields = ('display_related_aids',)

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
        related_aid_html = '<ul>'
        for aid in obj.financed_aids.all().order_by('name'):
            url = reverse("admin:aids_aid_change", args=(aid.pk,))
            related_aid_html += f'<li><a href="{url}">'
            related_aid_html += escape(aid.name)
            related_aid_html += f' (ID : {aid.pk})'
            related_aid_html += '</a></li>'
        related_aid_html += '</ul>'
        return mark_safe(related_aid_html)
    display_related_aids.short_description = _('Related aids')

admin.site.register(Backer, BackerAdmin)
