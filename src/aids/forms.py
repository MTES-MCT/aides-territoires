import re
import operator
from functools import reduce
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
            'destinations': _('The aid is destined to…'),
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

    SCALES = (
        (1, _('Commune')),
        (5, _('EPCI')),
        (10, _('Department')),
        (15, _('Region')),
        (20, _('France')),
        (25, _('Europe')),
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
        label=_('When to mobilize the aid?'),
        required=False,
        choices=Aid.STEPS)
    destinations = forms.MultipleChoiceField(
        label=_('Destinations'),
        required=False,
        choices=Aid.DESTINATIONS)
    scale = forms.MultipleChoiceField(
        label=_('Diffusion scale'),
        required=False,
        choices=SCALES)
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

        scale = self.cleaned_data.get('scale', None)
        if scale:
            qs = qs.filter(perimeter__scale__in=scale)

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

        # Here is where the "free text search" is handled, using postgresql's
        # great fulltext features.
        #
        # In Postgres, you converts a search query into a `tsquery` object
        # that is matched against a `tsvector` object.
        #
        # There are two main methods to get a `tsquery`. The first is to use
        # the function `plainto_tsquery` that is designed to transform
        # unformatted text and generates a `tsquery` with tokens separated by
        # `AND`. That is the default function used by Django when you create
        # a `SearchQuery` object.
        #
        # The second method is to use the `to_tsquery` method. This method
        # takes a query that is already formatted with tokens and binary
        # operators. You cannot pass raw user queries to this method or you
        # *will* get errors. That is the method used by Django when you add the
        # `search_type='raw' parameter.
        #
        # At the beginning, we used a simple `plainto_tsquery` but when the
        # need to offer a more powerful search syntax arrised, we switched to
        # `to_tsquery` and had to manually parse the users' queries.
        text = self.cleaned_data.get('text', None)
        if text:
            query = self.parse_query(text)
            qs = qs \
                .filter(search_vector=query) \
                .annotate(rank=SearchRank(F('search_vector'), query))

        return qs

    def parse_query(self, raw_query):
        """Process a raw query and returns a `SearchQuery`.

        By default, search terms are optional.
        A term prefixed by "+" becomes mandatory.
        A term prefixed by "-" is excluded from results.
        """
        or_terms = []
        and_terms = []
        not_terms = []
        all_terms = raw_query.split(' ')
        for term in all_terms:
            if term.startswith('+'):
                and_terms.append(term.lstrip('+'))
            elif term.startswith('-'):
                not_terms.append(term.lstrip('-'))
            else:
                or_terms.append(term)

        or_query = reduce(
            operator.or_,
            [SearchQuery(or_term, config='french') for or_term in or_terms]
        ) if or_terms else None

        not_query = reduce(
            operator.and_,
            [~SearchQuery(not_term, config='french') for not_term in not_terms]
        ) if not_terms else None

        and_query = reduce(
            operator.and_,
            [SearchQuery(and_term, config='french') for and_term in and_terms]
        ) if and_terms else None

        search_query_parts = filter(None, [and_query, or_query])
        search_query = reduce(operator.and_, search_query_parts)

        if not_query:
            query = not_query & search_query
        else:
            query = search_query

        return query

    def order_queryset(self, qs):
        """Set the order value on the queryset.

        We scale results by perimeter scale, unless the user submitted a
        search query, then we sort by query relevance.
        """
        text = self.cleaned_data.get('text', None)
        if text:
            qs = qs.order_by(
                '-rank', 'perimeter__scale', 'submission_deadline')
        else:
            qs = qs.order_by('perimeter__scale', 'submission_deadline')
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
