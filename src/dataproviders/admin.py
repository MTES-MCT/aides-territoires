from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from dataproviders.models import DataSource


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    raw_id_fields = ('perimeter', 'backer', 'contact_team')