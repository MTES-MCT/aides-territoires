from django.contrib import admin
from django import forms

from geofr.models import Perimeter


class PerimeterAdminForm(forms.ModelForm):
    class Meta:
        fields = ['code', 'name']


class PerimeterAdmin(admin.ModelAdmin):
    """Admin module for perimeters."""

    list_display = ('scale', 'name', 'manually_created', 'code', 'is_overseas',
                    'regions', 'departments', 'epci', 'zipcodes', 'basin')
    search_fields = ['name', 'code']
    list_filter = ('scale', 'is_overseas', 'manually_created')
    ordering = ('-scale', 'name')
    form = PerimeterAdminForm

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.manually_created
        return False

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.manually_created
        return False

    def save_model(self, request, obj, form, change):
        """Handle perimeter manual creations.

        Only adhoc perimeters can be created. Other perimeters are imported
        from the geo api or other official data sources.
        """
        obj.manually_created = True
        obj.scale = Perimeter.TYPES.adhoc
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Add France and Europe perimeters to new adhoc perimeters."""

        if not change:
            perimeters = Perimeter.objects.filter(scale__in=(
                Perimeter.TYPES.continent, Perimeter.TYPES.country
            ))
            obj = form.instance
            obj.contained_in.add(*perimeters)

        super().save_related(request, form, formsets, change)


admin.site.register(Perimeter, PerimeterAdmin)
