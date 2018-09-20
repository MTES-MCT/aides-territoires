from django.contrib import admin
from django.db.models import Count

from backers.models import Backer


class AidInline(admin.TabularInline):
    model = Backer.aids.through
    extra = 0


class BackerAdmin(admin.ModelAdmin):
    """Admin module for aid backers."""

    list_display = ['name', 'nb_aids']
    search_fields = ['name']
    inlines = [AidInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(nb_aids=Count('aids'))
        return qs

    def nb_aids(self, obj):
        return obj.nb_aids


admin.site.register(Backer, BackerAdmin)
