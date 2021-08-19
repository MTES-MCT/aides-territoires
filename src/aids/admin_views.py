from django.views.generic import UpdateView
from django.http import Http404
from django.forms import modelform_factory
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from aids.templatetags.amendments import extract_value
from aids.forms import AidEditForm
from aids.models import Aid


class AmendmentMerge(SuccessMessageMixin, UpdateView):
    """Display a form to merge an amendment data into the amended aid."""

    template_name = 'admin/amend_ui.html'
    pk_url_kwarg = 'object_id'
    context_object_name = 'aid'
    success_url = reverse_lazy('admin:aids_amendment_changelist')
    success_message = "L'aide a bien été mise à jour."

    def get_queryset(self):
        qs = Aid.amendments.all() \
            .select_related('amended_aid')
        return qs

    def get_object(self):
        """The `object` edited in the form is the amended aid."""
        pk = self.kwargs.get(self.pk_url_kwarg)
        qs = Aid.amendments.all()
        try:
            amendment = qs.get(pk=pk)
        except Aid.DoesNotExist:
            raise Http404('')

        # Also store the amendment targeted in the url
        self.amendment = amendment
        aid = amendment.amended_aid
        return aid

    def get_diff_fields(self):
        """Return fields with differences between the aid and the amendment."""

        def has_diff(field_name):
            """Is there a difference for this value?.

            Compares the value for `field_name`, for the aid and the amendment.
            """
            v1 = extract_value(self.object, field_name)
            v2 = extract_value(self.amendment, field_name)
            return v1 != v2

        all_fields = AidEditForm._meta.fields
        diff_fields = list(filter(has_diff, all_fields))
        return diff_fields

    def get_form_class(self):
        """Build an aid edit form with only amended fields."""
        diff_fields = self.get_diff_fields()
        AidForm = modelform_factory(Aid, form=AidEditForm, fields=diff_fields)
        return AidForm

    def get_form(self):
        """Return an instanciated form.

        For some reasons, the `fields` paramameter of the `modelform_factory`
        method is not enough to exclude unwanted fields. Fields that are added
        declaratively in the original form class are still present. Hence,
        we have to remove them manually. This is quite hackish.
        """
        form = super().get_form()
        diff_fields = self.get_diff_fields()
        fields = list(form.fields)
        for field in fields:
            if field not in diff_fields:
                del form.fields[field]

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'amendment': self.amendment,
        })
        return context

    def form_valid(self, form):
        res = super().form_valid(form)
        self.amendment.delete()
        return res
