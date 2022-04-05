from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from braces.views import MessageMixin

from geofr.models import Perimeter
from geofr.forms import PerimeterUploadForm, PerimeterCombineForm
from geofr.utils import (attach_perimeters_check, extract_perimeters_from_file,
                         attach_epci_perimeters,
                         combine_perimeters)

import logging

logger = logging.getLogger('console_log')
logger.setLevel(logging.DEBUG)


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

            result = attach_perimeters_check(
                current_perimeter,
                city_codes,
                self.request.user,
                logger)

        elif perimeter_type == 'epci_name':
            # Fetch the list of EPCI perimeters from the uploaded file
            # The list should be error-free (cleaned in PerimeterUploadForm)
            epci_names = extract_perimeters_from_file(
                form.cleaned_data['epci_name_list'])
            result = attach_epci_perimeters(current_perimeter, epci_names, self.request.user)

        if result['method'] == 'delayed import':
            msg = "Votre périmètre est en cours de création. \
                Veuillez s’il vous plaît contacter l’équipe dev."
        else:
            msg = "Votre périmètre a été créé avec succès."
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
        city_codes = list(combine_perimeters(add_perimeters, rm_perimeters))
        result = attach_perimeters_check(current_perimeter, city_codes, self.request.user)

        if result['method'] == 'delayed import':
            msg = "Votre périmètre est en cours de création. \
                Veuillez s’il vous plaît contacter l’équipe dev."
        else:
            msg = "Votre périmètre a été créé avec succès."
        self.messages.success(msg)

        return super().form_valid(form)
