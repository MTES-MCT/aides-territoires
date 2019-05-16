import re
import operator
from datetime import timedelta

from django import forms
from django.db.models import Q, F
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.postgres.search import SearchQuery, SearchRank

from core.forms.widgets import (AutocompleteSelectMultiple,
                                MultipleChoiceFilterWidget)
from backers.models import Backer
from geofr.models import Perimeter
from geofr.forms.fields import PerimeterChoiceField
from tags.fields import TagChoiceField
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
    tags = TagChoiceField(
        label=_('Tags'),
        choices=list,
        required=False)

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

        # We set the existing tags as the `choices` value so the existing
        # tags will be displayed in the widget
        all_tags = self.instance.tags
        if self.is_bound:
            if hasattr(self.data, 'getlist'):
                all_tags += self.data.getlist('tags')
            else:
                all_tags += self.data.get('tags', [])
        self.fields['tags'].choices = zip(all_tags, all_tags)

        custom_labels = {
            'name': _('Aid title'),
            'targeted_audiances': _('Who can apply to this aid?'),
            'backers': _('Aid backers'),
            'new_backer': _('…or add a new backer'),
            'destinations': _('Types of expenses covered'),
            'eligibility': _('Are the any other eligibility criterias?'),
            'origin_url': _('Link to a full description'),
            'application_url': _('Link to an online application form'),
            'contact_detail': _('Name of a contact in charge'),
            'contact_email': _('E-mail address of a contact in charge'),
            'contact_phone': _('Phone number of a contact in charge'),
            'is_call_for_project': _('Is this a call for project / expressions'
                                     ' of interest?')
        }
        for field, label in custom_labels.items():
            self.fields[field].label = label

        custom_help_text = {
            'tags': _('Add up to 16 keywords to describe your aid'
                      ' (separated by ",")'),
            'new_backer': _('If the aid backer is not in the previous list, '
                            'use this field to add a new one.'),
        }
        for field, help_text in custom_help_text.items():
            self.fields[field].help_text = help_text

    def save(self, commit=True):
        """Saves the instance.

        We update the aid search_vector here, because this is the only place
        we gather all the necessary data (object + m2m related objects).
        """
        backers = self.cleaned_data['backers']
        self.instance.set_search_vector(backers)
        return super().save(commit=commit)

    def _save_m2m(self):
        super()._save_m2m()
        self.instance.populate_tags()


class AidAdminForm(BaseAidForm):
    """Custom Aid edition admin form."""

    class Media:
        js = ['admin/js/tags_autocomplete.js']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['class'] = 'admin-autocomplete'


class AidSearchForm(forms.Form):
    """Main form for search engine."""

    AID_CATEGORY_CHOICES = (
        ('', ''),
        ('funding', _('Funding')),
        ('non-funding', _('Non-funding')),
    )

    ORDER_BY = (
        ('relevance', _('Relevance')),
        ('publication_date', _('Publication date')),
        ('submission_deadline', _('Submission deadline')),
    )

    perimeter = PerimeterChoiceField(
        label=_('Your project\'s location'),
        required=False)
    text = forms.CharField(
        label=_('Text search'),
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Aid title, keyword, etc.')}))
    # We use a multiple choice field so the filter rendering remains
    # consistent with the other filters
    recent_only = forms.MultipleChoiceField(
        label=_('Recent aids'),
        choices=(
            (_('Yes'), _('Only display aids created less than 30 days ago')),),
        required=False,
        widget=MultipleChoiceFilterWidget)
    apply_before = forms.DateField(
        label=_('Apply before…'),
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': _('yyyy-mm-dd')}))
    aid_types = forms.MultipleChoiceField(
        label=_('Aid type'),
        required=False,
        choices=AID_TYPES)
    mobilization_step = forms.MultipleChoiceField(
        label=_('Project progress'),
        required=False,
        choices=Aid.STEPS)
    destinations = forms.MultipleChoiceField(
        label=_('Concerned actions'),
        required=False,
        choices=Aid.DESTINATIONS)
    call_for_projects_only = forms.MultipleChoiceField(
        label=_('Call for projects'),
        choices=((
            _('Yes'),
            _('Only show calls for project / expressions of interest')),),
        required=False,
        widget=MultipleChoiceFilterWidget)

    # This field is not related to the search, but is submitted
    # in views embedded through an iframe.
    integration = forms.CharField(
        required=False,
        widget=forms.HiddenInput)

    # This field is used to sort results
    order_by = forms.ChoiceField(
        label=_('Order by'),
        required=False,
        choices=ORDER_BY)

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        if zipcode and re.match(r'\d{5}', zipcode) is None:
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

        apply_before = self.cleaned_data.get('apply_before', None)
        if apply_before:
            qs = qs.filter(submission_deadline__lt=apply_before)

        recent_only = self.cleaned_data.get('recent_only', False)
        if recent_only:
            a_month_ago = timezone.now() - timedelta(days=30)
            qs = qs.filter(date_created__gte=a_month_ago.date())

        call_for_projects_only = self.cleaned_data.get(
            'call_for_projects_only', False)
        if call_for_projects_only:
            qs = qs.filter(is_call_for_project=True)

        text = self.cleaned_data.get('text', None)
        if text:
            query = self.parse_query(text)
            qs = qs \
                .filter(search_vector=query) \
                .annotate(rank=SearchRank(F('search_vector'), query))

        return qs

    def parse_query(self, raw_query):
        """Process a raw query and returns a `SearchQuery`.

        In Postgres, you converts a search query into a `tsquery` object
        that is matched against a `tsvector` object.

        The main method to get a `tsquery` is to use
        the function `plainto_tsquery` that is designed to transform
        unformatted text and generates a `tsquery` with tokens separated by
        `AND`. That is the default function used by Django when you create
        a `SearchQuery` object.

        If you want to create a `ts_query` with other boolean operators, you
        have two main solutions:
         - use the `to_tsquery` method that is not made to handle raw data
         - create several `ts_query` objects and combine them using
           boolean operators.

        This is the second solution we are using.

        By default, terms are optional.
        Terms with a "+" in between are made mandatory.
        Terms preceded with a "-" are filtered out.
        """
        all_terms = filter(None, raw_query.split(' '))
        next_operator = operator.or_
        invert = False
        query = None

        for term in all_terms:
            if term == '+':
                next_operator = operator.and_
                continue

            if term == '-':
                next_operator = operator.and_
                invert = True
                continue

            if query is None:
                query = SearchQuery(term, config='french', invert=invert)
            else:
                query = next_operator(query, SearchQuery(
                    term, config='french', invert=invert))

            next_operator = operator.or_
            invert = False

        return query

    def order_queryset(self, qs):
        """Set the order value on the queryset."""

        # Default results order
        # We show the narrower perimet first, then aids with a deadline
        order_fields = ['perimeter__scale', 'submission_deadline']

        # If the user submitted a text query, we order by query rank first
        text = self.cleaned_data.get('text', None)
        if text:
            order_fields = ['-rank'] + order_fields

        # If the user requested a manual order by publication date
        manual_order = self.cleaned_data.get('order_by', 'relevance')
        if manual_order == 'publication_date':
            order_fields = ['-date_created'] + order_fields
        elif manual_order == 'submission_deadline':
            order_fields = ['submission_deadline'] + order_fields

        qs = qs.order_by(*order_fields)
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

        Some perimeters must be handled as special cases:

         - Overseas: every overseas perimeters ;
         - Mailand: every perimeter that is NOT overseas.
        """

        # Since we only handle french aids, searching for european or
        # national aids will return all results
        if perimeter.scale in (Perimeter.TYPES.country,
                               Perimeter.TYPES.continent):
            return qs

        # Special case: overseas only
        if perimeter.scale == Perimeter.TYPES.overseas:
            qs = qs.filter(perimeter__is_overseas=True)
            return qs

        # Special case: mainland only
        if perimeter.scale == Perimeter.TYPES.mainland:
            qs = qs.filter(perimeter__is_overseas=False)
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
        widget=AutocompleteSelectMultiple,
        required=False)
    perimeter = PerimeterChoiceField(
        label=_('Perimeter'))

    class Meta(BaseAidForm.Meta):
        model = Aid
        fields = [
            'name',
            'description',
            'tags',
            'targeted_audiances',
            'backers',
            'new_backer',
            'recurrence',
            'start_date',
            'predeposit_date',
            'submission_deadline',
            'perimeter',
            'is_call_for_project',
            'aid_types',
            'subvention_rate',
            'mobilization_steps',
            'destinations',
            'eligibility',
            'origin_url',
            'application_url',
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

    def clean(self):
        """Make sure the aid backers were provided."""

        data = self.cleaned_data
        if not any((data.get('backers'), data.get('new_backer'))):
            msg = _('You must select the aid backers, or create a new one '
                    'below.')
            self.add_error('backers', msg)

        return data
