from django.contrib import admin
from django.db.models import Count

from dataproviders.models import DataSource


class DataSourceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "contact_team",
        "aid_author",
        "nb_aids",
        "date_last_access",
    ]
    list_filter = ["contact_team"]

    autocomplete_fields = ["backer", "perimeter", "contact_team", "aid_author"]
    readonly_fields = ["date_created", "date_updated", "date_last_access"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("backer", "perimeter", "contact_team").annotate(
            aid_count=Count("aids")
        )
        return qs

    def nb_aids(self, data_source):
        return data_source.aid_count

    nb_aids.short_description = "Nombre d'aides"
    nb_aids.admin_order_field = "aid_count"


admin.site.register(DataSource, DataSourceAdmin)
