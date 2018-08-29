import re

from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from aids.models import Aid
from geofr.utils import (is_overseas, department_from_zipcode,
                         region_from_zipcode)


class AidAdminForm(forms.ModelForm):
    """Custom form form Aids in admin."""

    class Meta:
        widgets = {
            'mobilization_steps': forms.CheckboxSelectMultiple,
            'targeted_audiances': forms.CheckboxSelectMultiple,
            'aid_types': forms.CheckboxSelectMultiple,
            'destinations': forms.CheckboxSelectMultiple,
            'thematics': forms.CheckboxSelectMultiple,
        }

    def clean(self):
        data = super().clean()

        application_perimeter = data.get('application_perimeter')
        department = data.get('application_department')
        region = data.get('application_region')

        # Let's make sure that all the required data is set
        if application_perimeter == Aid.PERIMETERS.department:
            if not department:
                msg = _('You must provided the application department.')
                self.add_error('application_department', msg)
        else:
            if department:
                msg = _('This value must be blank.')
                self.add_error('application_department', msg)

        if application_perimeter == Aid.PERIMETERS.region:
            if not region:
                msg = _('You must provided the application region.')
                self.add_error('application_region', msg)
        else:
            if region:
                msg = _('This value must be blank.')
                self.add_error('application_region', msg)

        return data


class MultipleChoiceFilterWidget(forms.widgets.CheckboxSelectMultiple):
    """A basic multi checkbox widget with a custom template.

    We can't override the default template because it would mess with the
    django admin.
    """

    template_name = 'forms/widgets/multiple_input.html'


class AidSearchForm(forms.Form):
    """Main form for search engine."""

    AID_CATEGORY_CHOICES = (
        ('', ''),
        ('funding', _('Funding')),
        ('non-funding', _('Non-funding')),
    )

    STEPS = (
        ('', ''),
    ) + Aid.STEPS

    # Subset of aid types
    TYPES = (
        (_('Funding aids'), (
            ('grant', _('Grant')),
            ('loan', _('Loan')),
            ('recoverable_advance', _('Recoverable advance')),
            ('interest_subsidy', _('Interest subsidy')),
        )),
        (_('Technical and methodological aids'), (
            ('guidance', _('Guidance')),
            ('networking', _('Networking')),
            ('valorisation', _('Valorisation')),
        )),
    )

    zipcode = forms.CharField(
        label=_('Zip code'),
        required=False,
        max_length=8)
    mobilization_step = forms.ChoiceField(
        label=_('When to mobilize the aid?'),
        required=False,
        choices=STEPS)
    aid_types = forms.MultipleChoiceField(
        label=_('Aid type'),
        required=False,
        choices=TYPES,
        widget=MultipleChoiceFilterWidget)
    destinations = forms.MultipleChoiceField(
        label=_('Destinations'),
        required=False,
        choices=Aid.DESTINATIONS,
        widget=MultipleChoiceFilterWidget)
    thematics = forms.MultipleChoiceField(
        label=_('Thematics'),
        required=False,
        choices=Aid.THEMATICS,
        widget=MultipleChoiceFilterWidget)
    scale = forms.MultipleChoiceField(
        label=_('Scale'),
        required=False,
        choices=Aid.PERIMETERS,
        widget=MultipleChoiceFilterWidget)
    apply_before = forms.DateField(
        label=_('Apply before…'),
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': _('yyyy-mm-dd')}))

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        if zipcode and re.match('\d{5}', zipcode) is None:
            msg = _('This zipcode seems invalid')
            raise forms.ValidationError(msg)

        return zipcode

    def filter_queryset(self, qs):
        """Filter querysets depending of input data."""

        if not self.is_bound:
            return qs

        # Populate cleaned_data
        if self.errors:
            pass

        zipcode = self.cleaned_data.get('zipcode', None)
        if zipcode:
            if is_overseas(zipcode):
                qs = qs.exclude(application_perimeter=Aid.PERIMETERS.mainland)
            else:
                qs = qs.exclude(application_perimeter=Aid.PERIMETERS.overseas)

            department_code = department_from_zipcode(zipcode)
            qs = qs.exclude(
                Q(application_perimeter=Aid.PERIMETERS.department) &
                ~Q(application_department=department_code))

            region_code = region_from_zipcode(zipcode)
            qs = qs.exclude(
                Q(application_perimeter=Aid.PERIMETERS.region) &
                ~Q(application_region=region_code))

        mobilization_step = self.cleaned_data.get('mobilization_step', None)
        if mobilization_step:
            qs = qs.filter(mobilization_steps__contains=[mobilization_step])

        aid_types = self.cleaned_data.get('aid_types', None)
        if aid_types:
            qs = qs.filter(aid_types__overlap=aid_types)

        destinations = self.cleaned_data.get('destinations', None)
        if destinations:
            qs = qs.filter(destinations__overlap=destinations)

        thematics = self.cleaned_data.get('thematics', None)
        if thematics:
            qs = qs.filter(thematics__overlap=thematics)

        scale = self.cleaned_data.get('scale', None)
        if scale:
            qs = qs.filter(application_perimeter__in=scale)

        apply_before = self.cleaned_data.get('apply_before', None)
        if apply_before:
            qs = qs.filter(submission_deadline__lt=apply_before)

        return qs
