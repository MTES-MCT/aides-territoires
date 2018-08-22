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

    zipcode = forms.CharField(
        label=_('Zip code'),
        required=False,
        max_length=8)
    aid_category = forms.ChoiceField(
        label=_('Funding / non-funding'),
        required=False,
        choices=AID_CATEGORY_CHOICES)
    mobilization_step = forms.ChoiceField(
        label=_('When to mobilize the aid?'),
        required=False,
        choices=STEPS)
    aid_types = forms.MultipleChoiceField(
        label=_('Aid type'),
        required=False,
        choices=Aid.TYPES,
        widget=forms.CheckboxSelectMultiple)
    destinations = forms.MultipleChoiceField(
        label=_('Destinations'),
        required=False,
        choices=Aid.DESTINATIONS,
        widget=forms.CheckboxSelectMultiple)
    thematics = forms.MultipleChoiceField(
        label=_('Thematics'),
        required=False,
        choices=Aid.THEMATICS,
        widget=forms.CheckboxSelectMultiple)
    scale = forms.MultipleChoiceField(
        label=_('Scale'),
        required=False,
        choices=Aid.PERIMETERS,
        widget=forms.CheckboxSelectMultiple)

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

        aid_category = self.cleaned_data.get('aid_category', None)
        if aid_category:
            if aid_category == 'funding':
                qs = qs.filter(is_funding=True)
            else:
                qs = qs.filter(is_funding=False)

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

        return qs
