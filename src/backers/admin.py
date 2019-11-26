from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from backers.models import Backer


class AidInline(admin.TabularInline):
    model = Backer.financers_aids.through
    extra = 0


class BackerAdmin(admin.ModelAdmin):
    """Admin module for aid backers."""

    list_display = ['name', 'is_corporate', 'nb_aids']
    search_fields = ['name']
    inlines = [AidInline]
    ordering = ['name']
    filter_fields = ['is_corporate']
    list_editable = ['is_corporate']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(nb_aids=Count('aids'))
        return qs

    def nb_aids(self, obj):
        return obj.nb_aids
    nb_aids.short_description = _('Number of aids')
    nb_aids.admin_order_field = 'nb_aids'


admin.site.register(Backer, BackerAdmin)
