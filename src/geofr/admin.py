from django import forms
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

from geofr.models import Perimeter
from geofr.admin_views import PerimeterUpload, PerimeterCombine


class PerimeterAdminForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'code', 'is_visible_to_users']


class PerimeterAdmin(admin.ModelAdmin):
    """Admin module for perimeters."""

    form = PerimeterAdminForm
    list_display = [
        'id', 'scale', 'name', 'manually_created', 'is_visible_to_users',
        'code', 'is_overseas',
        'regions', 'departments', 'epci', 'zipcodes', 'basin']
    list_filter = [
        'scale', 'is_overseas', 'manually_created', 'is_visible_to_users']
    search_fields = ['id', 'name', 'code']
    ordering = ['-date_created']
    # readonly_fields ? managed below

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    def get_readonly_fields(self, request, obj=None):
        """
        All fields are readonly except:
        - Allow name is_visible_to_users edition for new or adhoc perimeters
        - Allow code edition for new or manually_created perimeters
        """
        readonly_fields = [f.name for f in Perimeter._meta.fields]
        if not obj or (obj.scale == Perimeter.SCALES.adhoc):
            readonly_fields.remove('name')
            readonly_fields.remove('is_visible_to_users')
        if not obj or obj.manually_created:
            readonly_fields.remove('code')
        return readonly_fields

    def get_changeform_initial_data(self, request):
        """Set is_visible_to_users to False for new perimeters"""
        initial = super(PerimeterAdmin, self).get_changeform_initial_data(request)  # noqa
        initial['is_visible_to_users'] = False
        return initial

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj and request.user.is_superuser:
            return obj.manually_created
        return False

    def save_model(self, request, obj, form, change):
        """Handle perimeter manual creations.

        Only adhoc perimeters can be created. Other perimeters are imported
        from the geo api or other official data sources.
        """
        obj.manually_created = True
        obj.scale = Perimeter.SCALES.adhoc
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Add France and Europe perimeters to new adhoc perimeters."""

        if not change:
            perimeters = Perimeter.objects.filter(scale__in=(
                Perimeter.SCALES.continent, Perimeter.SCALES.country
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
            path(
                _('<path:object_id>/combine/'),
                self.admin_site.admin_view(self.perimeter_combine_view),
                name='geofr_perimeter_combine'),

        ]
        return my_urls + urls

    def perimeter_upload_view(self, request, object_id=None):
        """Display the form to upload a list of communes."""

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

    def perimeter_combine_view(self, request, object_id=None):
        """Display the form to combine several perimeters."""

        opts = self.model._meta
        app_label = opts.app_label
        obj = self.get_object(request, object_id)

        context = {
            **self.admin_site.each_context(request),
            'title': _('Perimeter combine'),
            'opts': opts,
            'app_label': app_label,
            'original': obj,
        }
        return PerimeterCombine.as_view(
            extra_context=context)(request, object_id=object_id)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        contained_perimeters = Perimeter.objects \
            .filter(contained_in__id=object_id) \
            .order_by('-scale', 'name')
        context = extra_context or {}
        context['contained_perimeters'] = contained_perimeters

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=context)


admin.site.register(Perimeter, PerimeterAdmin)
