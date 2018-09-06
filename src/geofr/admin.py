from django.contrib import admin

from geofr.models import Perimeter


class PerimeterAdmin(admin.ModelAdmin):
    """Admin module for perimeters."""

    list_display = ('scale', 'name', 'code', 'is_overseas', 'region',
                    'department', 'epci', 'zipcodes')
    search_fields = ['name']
    list_filter = ('scale', 'is_overseas')
    ordering = ('-scale', 'name')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False


admin.site.register(Perimeter, PerimeterAdmin)
