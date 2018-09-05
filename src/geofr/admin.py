from django.contrib import admin

from geofr.models import Perimeter


class PerimeterAdmin(admin.ModelAdmin):
    """Admin module for perimeters."""

    list_display = ('scale', 'name', 'code', 'region', 'department', 'epci',
                    'zipcodes')
    search_fields = ['name__search']
    list_filter = ('scale',)
    ordering = ('-scale', 'name')


admin.site.register(Perimeter, PerimeterAdmin)
