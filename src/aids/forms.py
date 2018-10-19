import re

from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from core.forms.widgets import AutocompleteSelectMultiple
from backers.models import Backer
from geofr.models import Perimeter
from geofr.forms.fields import PerimeterChoiceField
from aids.models import Aid


AID_TYPES = (
    (_('Financial aids'), (
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


class BaseAidForm(forms.ModelForm):
    class Meta:
        widgets = {
            'mobilization_steps': forms.CheckboxSelectMultiple,
            'targeted_audiances': forms.CheckboxSelectMultiple,
            'aid_types': forms.CheckboxSelectMultiple,
            'destinations': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['aid_types'].choices = AID_TYPES

        custom_labels = {
            'name': _('Aid title'),
            'targeted_audiances': _('Who can apply to this aid?'),
            'backers': _('Aid backers'),
            'destinations': _('The aid is destined to…'),
            'eligibility': _('Are the any other eligibility criterias?'),
            'url': _('Link to a full description'),
            'application_url': _('Link to an online application form'),
            'contact_detail': _('Name of a contact in charge'),
            'contact_email': _('E-mail address of a contact in charge'),
            'contact_phone': _('Phone number of a contact in charge'),
        }
        for field, label in custom_labels.items():
            self.fields[field].label = label


class AidAdminForm(BaseAidForm):
    """Custom form form Aids in admin."""
    pass


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

    SCALES = (
        (1, _('Commune')),
        (5, _('EPCI')),
        (10, _('Department')),
        (15, _('Region')),
        (20, _('France')),
        (25, _('Europe')),
    )

    perimeter = PerimeterChoiceField(
        label=_('Perimeter'),
        required=False)
    apply_before = forms.DateField(
        label=_('Apply before…'),
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': _('yyyy-mm-dd')}))
    aid_types = forms.MultipleChoiceField(
        label=_('Aid type'),
        required=False,
        choices=AID_TYPES,
        widget=MultipleChoiceFilterWidget)
    mobilization_step = forms.MultipleChoiceField(
        label=_('When to mobilize the aid?'),
        required=False,
        choices=Aid.STEPS,
        widget=MultipleChoiceFilterWidget)
    destinations = forms.MultipleChoiceField(
        label=_('Destinations'),
        required=False,
        choices=Aid.DESTINATIONS,
        widget=MultipleChoiceFilterWidget)
    scale = forms.MultipleChoiceField(
        label=_('Diffusion'),
        required=False,
        choices=SCALES,
        widget=MultipleChoiceFilterWidget)

    # This field is not related to the search, but is submitted
    # in views embedded through an iframe.
    integration = forms.CharField(
        required=False,
        widget=forms.HiddenInput)

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

        perimeter = self.cleaned_data.get('perimeter', None)
        if perimeter:
            qs = self.perimeter_filter(qs, perimeter)

        mobilization_steps = self.cleaned_data.get('mobilization_step', None)
        if mobilization_steps:
            qs = qs.filter(mobilization_steps__overlap=mobilization_steps)

        aid_types = self.cleaned_data.get('aid_types', None)
        if aid_types:
            qs = qs.filter(aid_types__overlap=aid_types)

        destinations = self.cleaned_data.get('destinations', None)
        if destinations:
            qs = qs.filter(destinations__overlap=destinations)

        scale = self.cleaned_data.get('scale', None)
        if scale:
            qs = qs.filter(perimeter__scale__in=scale)

        apply_before = self.cleaned_data.get('apply_before', None)
        if apply_before:
            qs = qs.filter(submission_deadline__lt=apply_before)

        return qs

    def perimeter_filter(self, qs, perimeter):
        """Filter queryset depending on the given perimeter.

        When we search for a given perimeter, we must return all aids:
         - where the perimeter is wider and contains the searched perimeter ;
         - where the perimeter is smaller and contained by the search
         perimeter ;

        E.g if we search for aids in "Hérault (department), we must display all
        aids that are applicable to:

         - Hérault ;
         - Occitanie ;
         - France ;
         - Europe ;
         - M3M (and all other epcis in Hérault) ;
         - Montpellier (and all other communes in Hérault) ;
        """

        # Since we only handle french aids, searching for european or
        # national aids will return all results
        if perimeter.scale in (Perimeter.TYPES.country,
                               Perimeter.TYPES.continent):
            return qs

        # Exclude all other perimeters from the same scale.
        # E.g We search for aids in "Herault", exclude all aids from other
        # departments.
        q_same_scale = Q(perimeter__scale=perimeter.scale)
        q_different_code = ~Q(perimeter__code=perimeter.code)
        qs = qs.exclude(q_same_scale & q_different_code)

        # Exclude all perimeters that are more granular and that are not
        # contained in the search perimeter.
        # E.g we search for aids in "Hérault", exclude communes and epcis that
        # are not in Hérault.
        if perimeter.scale > Perimeter.TYPES.commune:

            q_smaller_scale = Q(perimeter__scale__lt=perimeter.scale)

            if perimeter.scale == Perimeter.TYPES.region:
                q_not_contained = ~Q(
                    perimeter__regions__contains=[perimeter.code])

            if perimeter.scale == Perimeter.TYPES.department:
                q_not_contained = ~Q(
                    perimeter__departments__contains=[perimeter.code])

            if perimeter.scale == Perimeter.TYPES.basin:
                # Edge case, when we search by drainage basins, don't
                # show aids from departments and regions, because that poorly
                # overlaps.
                qs = qs.exclude(perimeter__scale__in=(
                    Perimeter.TYPES.department,
                    Perimeter.TYPES.region))

                q_not_contained = ~Q(perimeter__basin=perimeter.code)

            if perimeter.scale == Perimeter.TYPES.epci:
                q_not_contained = ~Q(perimeter__epci=perimeter.code)

            qs = qs.exclude(q_smaller_scale & q_not_contained)

        # Exclude all perimeters that are wider and that does not
        # contain our search perimeter.
        # E.g we search for aids in "Hérault", exclude regions that are not
        # Occitanie.
        if perimeter.regions:
            q_scale_region = Q(perimeter__scale=Perimeter.TYPES.region)
            q_different_region = ~Q(perimeter__code__in=perimeter.regions)
            qs = qs.exclude(q_scale_region & q_different_region)

        if perimeter.departments:
            q_scale_department = Q(perimeter__scale=Perimeter.TYPES.department)
            q_different_department = ~Q(
                perimeter__code__in=perimeter.departments)
            qs = qs.exclude(q_scale_department & q_different_department)

        if perimeter.basin:
            q_scale_basin = Q(perimeter__scale=Perimeter.TYPES.basin)
            q_different_basin = ~Q(perimeter__code=perimeter.basin)
            qs = qs.exclude(q_scale_basin & q_different_basin)

        if perimeter.epci:
            q_scale_epci = Q(perimeter__scale=Perimeter.TYPES.epci)
            q_different_epci = ~Q(perimeter__code=perimeter.epci)
            qs = qs.exclude(q_scale_epci & q_different_epci)

        return qs


class AidEditForm(BaseAidForm):

    backers = forms.ModelMultipleChoiceField(
        label=_('Backers'),
        queryset=Backer.objects.all(),
        widget=AutocompleteSelectMultiple)
    perimeter = PerimeterChoiceField(
        label=_('Perimeter'))

    class Meta(BaseAidForm.Meta):
        model = Aid
        fields = [
            'name',
            'description',
            'targeted_audiances',
            'backers',
            'recurrence',
            'start_date',
            'predeposit_date',
            'submission_deadline',
            'perimeter',
            'aid_types',
            'subvention_rate',
            'mobilization_steps',
            'destinations',
            'eligibility',
            'application_url',
            'url',
            'contact_detail',
            'contact_email',
            'contact_phone',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'eligibility': forms.Textarea(attrs={'rows': 3}),
            'mobilization_steps': MultipleChoiceFilterWidget,
            'targeted_audiances': MultipleChoiceFilterWidget,
            'aid_types': MultipleChoiceFilterWidget,
            'destinations': MultipleChoiceFilterWidget,
            'start_date': forms.TextInput(
                attrs={'type': 'date', 'placeholder': _('yyyy-mm-dd')}),
            'predeposit_date': forms.TextInput(
                attrs={'type': 'date', 'placeholder': _('yyyy-mm-dd')}),
            'submission_deadline': forms.TextInput(
                attrs={'type': 'date', 'placeholder': _('yyyy-mm-dd')}),

        }
