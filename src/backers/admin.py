from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from backers.models import Backer


class AidInline(admin.TabularInline):
    model = Backer.financers_aids.through
    extra = 0


class BackerAdmin(admin.ModelAdmin):
    """Admin module for aid backers."""

    list_display = ['name', 'is_corporate', 'nb_financed_aids',
                    'nb_instructed_aids']
    search_fields = ['name']
    inlines = [AidInline]
    ordering = ['name']
    filter_fields = ['is_corporate']
    list_editable = ['is_corporate']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            nb_financed_aids=Count('financers_aids'),
            nb_instructed_aids=Count('instructors_aids')
        )
        return qs

    def nb_financed_aids(self, obj):
        return obj.nb_financed_aids
    nb_financed_aids.short_description = _('Financed aids')
    nb_financed_aids.admin_order_field = 'nb_financed_aids'

    def nb_instructed_aids(self, obj):
        return obj.nb_instructed_aids
    nb_instructed_aids.short_description = _('Instructed aids')
    nb_instructed_aids.admin_order_field = 'nb_instructed_aids'


admin.site.register(Backer, BackerAdmin)
