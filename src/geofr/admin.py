from django import forms
from django.contrib import admin
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from geofr.models import Perimeter
from geofr.admin_views import PerimeterUpload


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
    readonly_fields = ['contained_in']

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

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

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                _('<path:object_id>/upload/'),
                self.admin_site.admin_view(self.perimeter_upload_view),
                name='geofr_perimeter_upload'),
        ]
        return my_urls + urls

    def perimeter_upload_view(self, request, object_id=None):
        opts = self.model._meta
        app_label = opts.app_label
        obj = self.get_object(request, object_id)

        context = {
            **self.admin_site.each_context(request),
            'title': _('Perimeter upload'),
            'opts': opts,
            'app_label': app_label,
            'original': obj,
        }
        return PerimeterUpload.as_view(
            extra_context=context)(request, object_id=object_id)


admin.site.register(Perimeter, PerimeterAdmin)
