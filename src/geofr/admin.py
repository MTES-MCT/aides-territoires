from django.contrib import admin

from geofr.models import Perimeter


class PerimeterAdmin(admin.ModelAdmin):
    """Admin module for perimeters."""

    list_display = ('scale', 'name', 'code')


admin.site.register(Perimeter, PerimeterAdmin)
