from django.views.generic import UpdateView
from django.http import Http404
from django.forms import modelform_factory

from aids.forms import AidEditForm
from aids.models import Aid


class AmendmentMerge(UpdateView):
    template_name = 'admin/amend_ui.html'
    pk_url_kwarg = 'object_id'
    context_object_name = 'aid'

    def get_queryset(self):
        qs = Aid.amendments.all() \
            .select_related('amended_aid')
        return qs

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        qs = Aid.amendments.all()
        try:
            amendment = qs.get(pk=pk)
        except Aid.DoesNotExist:
            raise Http404('')

        self.amendment = amendment
        aid = amendment.amended_aid
        return aid

    def get_diff_fields(self):
        """Return fields with a difference."""

        def filter_field(field_name):
            v1 = getattr(self.object, field_name)
            v2 = getattr(self.amendment, field_name)
            return v1 != v2

        all_fields = AidEditForm._meta.fields
        diff_fields = list(filter(filter_field, all_fields))
        return diff_fields

    def get_form_class(self):
        diff_fields = self.get_diff_fields()
        AidForm = modelform_factory(Aid, form=AidEditForm, fields=diff_fields)
        return AidForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'amendment': self.amendment,
        })
        return context
