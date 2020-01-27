from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from braces.views import MessageMixin

from geofr.models import Perimeter
from geofr.forms import PerimeterUploadForm, PerimeterCombineForm
from geofr.utils import attach_perimeters, combine_perimeters


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

    def form_valid(self, form):
        # Fetch the list of commune perimeters from the uploaded file
        city_codes = []
        for line in form.cleaned_data['city_list']:
            try:
                code = line.decode().strip().split(';')[0]
                clean_code = str(code)
                city_codes.append(clean_code)
            except (UnicodeDecodeError, ValueError) as e:
                msg = _('This file seems invalid. \
                        Please double-check its content or contact the \
                        dev team if you feel like it\'s an error. \
                        Here is the original error: {}').format(e)
                self.messages.error(msg)
                return self.get(self.request, *self.args, **self.kwargs)

        current_perimeter = self.get_object()
        attach_perimeters(current_perimeter, city_codes)

        msg = _('We successfully updated the perimeters.')
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
            'admin:geofr_perimeter_change', args=[self.kwargs['object_id']])

    def form_valid(self, form):

        perimeter = self.get_object()
        add_perimeters = form.cleaned_data['add_perimeters']
        rm_perimeters = form.cleaned_data['rm_perimeters']
        city_codes = combine_perimeters(add_perimeters, rm_perimeters)
        attach_perimeters(perimeter, city_codes)

        msg = _('We successfully configured the perimeter.')
        self.messages.success(msg)
        return super().form_valid(form)
