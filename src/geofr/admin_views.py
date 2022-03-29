from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from braces.views import MessageMixin
from django.utils.safestring import mark_safe
from django.contrib import messages

from geofr.models import Perimeter
from geofr.forms import PerimeterUploadForm, PerimeterCombineForm
from geofr.utils import (extract_perimeters_from_file,
                         attach_epci_perimeters,
                         combine_perimeters)
from geofr.tasks import attach_perimeters_async


class PerimeterUpload(MessageMixin, SingleObjectMixin, FormView):
    """Gets a list of city codes and update the corresponding perimeters."""

    template_name = 'admin/perimeter_upload.html'
    pk_url_kwarg = 'object_id'
    context_object_name = 'perimeter'
    success_url = reverse_lazy('admin:geofr_perimeter_changelist')
    form_class = PerimeterUploadForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Perimeter.objects.all()
        return qs

    def post(self, request, *args, **kwargs):
        """needed to display form errors."""
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        current_perimeter = self.get_object()
        perimeter_type = form.cleaned_data['perimeter_type']

        if perimeter_type == 'city_code':
            # Fetch the list of commune perimeters from the uploaded file
            # The list should be error-free (cleaned in PerimeterUploadForm)
            city_codes = extract_perimeters_from_file(
                form.cleaned_data['city_code_list'])
            attach_perimeters_async.delay(current_perimeter.id, city_codes, self.request.user.id)

        elif perimeter_type == 'epci_name':
            # Fetch the list of EPCI perimeters from the uploaded file
            # The list should be error-free (cleaned in PerimeterUploadForm)
            epci_names = extract_perimeters_from_file(
                form.cleaned_data['epci_name_list'])
            attach_epci_perimeters(current_perimeter, epci_names)

        msg = format_html(
            _('The {name} “{obj}” was changed successfully.'),
            name=_('Perimeter'),
            obj=format_html(
                '<a href="{obj_url}">{obj_name}</a>',
                obj_url=reverse(
                    'admin:geofr_perimeter_change', args=[current_perimeter.id]
                ),
                obj_name=current_perimeter
            )
        )
        self.messages.success(msg)
        return super().form_valid(form)


class PerimeterCombine(MessageMixin, SingleObjectMixin, FormView):
    """Create a new perimeter by combining other perimeters."""

    template_name = 'admin/perimeter_combine.html'
    pk_url_kwarg = 'object_id'
    context_object_name = 'perimeter'
    form_class = PerimeterCombineForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_queryset(self):
        qs = Perimeter.objects.all()
        return qs

    def get_success_url(self):
        return reverse_lazy(
            'admin:geofr_perimeter_change', args=[self.kwargs['object_id']]
        )

    def form_valid(self, form):
        current_perimeter = self.get_object()
        add_perimeters = form.cleaned_data['add_perimeters']
        rm_perimeters = form.cleaned_data['rm_perimeters']
        city_codes = combine_perimeters(add_perimeters, rm_perimeters)
        attach_perimeters_async.delay(current_perimeter, city_codes)
        messages.info(request, "Votre périmètre est en cours de création")

        msg = _('We successfully configured the perimeter.')
        self.messages.success(msg)
        return super().form_valid(form)
