from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from geofr.models import Perimeter
from geofr.forms import PerimeterUploadForm


class PerimeterUpload(SuccessMessageMixin, SingleObjectMixin, FormView):
    """Gets a list of city codes and update the corresponding perimeters."""

    template_name = 'admin/perimeter_upload.html'
    pk_url_kwarg = 'object_id'
    context_object_name = 'perimeter'
    success_url = reverse_lazy('admin:geofr_perimeter_changelist')
    success_message = _('The perimeter was successfully updated')
    form_class = PerimeterUploadForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Perimeter.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Delete existing link between this perimeter and others
        current_perimeter = self.get_object()
        PerimeterContainedIn = Perimeter.contained_in.through
        PerimeterContainedIn.objects \
            .filter(to_perimeter_id=current_perimeter.id) \
            .delete()

        # Fetch the list of commune perimeters from the uploaded file
        city_codes = [
            c.decode().strip() for c in form.cleaned_data['city_list']]
        perimeters = Perimeter.objects \
            .filter(code__in=city_codes) \
            .filter(scale=Perimeter.TYPES.commune) \
            .prefetch_related('contained_in')

        # Create the links between perimeters
        containing = []
        for perimeter in perimeters:
            containing.append(PerimeterContainedIn(
                from_perimeter_id=perimeter.id,
                to_perimeter_id=current_perimeter.id))

            for container in perimeter.contained_in.all():
                if container != current_perimeter:
                    containing.append(PerimeterContainedIn(
                        from_perimeter_id=container.id,
                        to_perimeter_id=current_perimeter.id))

        PerimeterContainedIn.objects.bulk_create(
            containing, ignore_conflicts=True)

        return super().form_valid(form)