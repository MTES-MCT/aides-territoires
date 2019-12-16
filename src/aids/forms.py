import re
import operator

from django import forms
from django.db.models import Q, F
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.postgres.search import SearchQuery, SearchRank

from core.forms import (
    AutocompleteSelectMultiple, MultipleChoiceFilterWidget, RichTextField)
from backers.models import Backer
from geofr.forms.fields import PerimeterChoiceField
from tags.fields import TagChoiceField
from categories.fields import CategoryMultipleChoiceField
from aids.models import Aid


FINANCIAL_AIDS = (
    ('grant', _('Grant')),
    ('loan', _('Loan')),
    ('recoverable_advance', _('Recoverable advance')),
    ('other', _('Other')),
)

TECHNICAL_AIDS = (
    ('technical', _('Technical')),
    ('financial', _('Financial')),
    ('legal', _('Legal')),
)

AID_TYPES = (
    (_('Financial aids'), FINANCIAL_AIDS),
    (_('Technical and methodological aids'), TECHNICAL_AIDS),
)

COLLECTIVITIES_AUDIANCES = (
    ('commune', _('Communes')),
    ('epci', _('Audiance EPCI')),
    ('department', _('Departments')),
    ('region', _('Regions')),
)

OTHER_AUDIANCES = (
    ('association', _('Associations')),
    ('private_person', _('Individuals')),
    ('farmer', _('Farmers')),
    ('private_sector', _('Private sector')),
    ('public_org', _('Public organizations')),
    ('lessor', _('Audiance lessors')),
    ('researcher', _('Research')),
)

AUDIANCES = (
    (_('Collectivities'), COLLECTIVITIES_AUDIANCES),
    (_('Other audiances'), OTHER_AUDIANCES)
)


CONTACT_INITIAL = '''
    <ul>
        <li>{}</li>
        <li>{}</li>
        <li>{}</li>
        <li>{}</li>
    </ul>
    '''.format(
        _('First / last name: '),
        _('Email: '),
        _('Phone: '),
        _('Comments: '),
    )


class BaseAidForm(forms.ModelForm):

    tags = TagChoiceField(
        label=_('Tags'),
        choices=list,
        required=False)
    description = RichTextField(
        label=_('Full description of the aid and its objectives'),
        widget=forms.Textarea(attrs={'placeholder': _(
            'If you have a description, do not hesitate to copy it here.\n'
            'Try to complete the description with the maximum of'
            ' information.\n'
            'If you are contacted regularly to ask for the same information,'
            ' try to give some answers in this space.')}))
    eligibility = RichTextField(
        label=_('Are the any other eligibility criterias?'),
        required=False)
    contact = RichTextField(
        label=_('Contact'),
        required=False,
        initial=CONTACT_INITIAL,
        help_text=_('Feel free to add several contacts'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'aid_types' in self.fields:
            self.fields['aid_types'].choices = AID_TYPES

        if 'targeted_audiances' in self.fields:
            self.fields['targeted_audiances'].choices = AUDIANCES

        if 'recurrence' in self.fields:
            self.fields['recurrence'].required = True

        # We set the existing tags as the `choices` value so the existing
        # tags will be displayed in the widget
        if 'tags' in self.fields:
            all_tags = self.instance.tags
            if self.is_bound:
                if hasattr(self.data, 'getlist'):
                    all_tags += self.data.getlist('tags')
                else:
                    all_tags += self.data.get('tags', [])
            all_tags = list(set(all_tags))
            self.fields['tags'].choices = zip(all_tags, all_tags)

        custom_labels = {
            'name': _('Aid title'),
            'financers': _('Aid financer(s)'),
            'instructors': _('Aid instructor(s)'),
            'new_backer': _('…or add a new financer'),
            'destinations': _('Types of expenses covered'),
            'origin_url': _('Link to a full description'),
            'application_url': _('Link to an online application form'),
            'is_call_for_project': _('Is this a call for project / expressions'
                                     ' of interest?')
        }
        for field, label in custom_labels.items():
            if field in self.fields:
                self.fields[field].label = label

        custom_help_text = {
            'new_backer':
                _('If the aid backer is not in the previous list, use this '
                  'field to add a new one.'),
            'tags': _('Add up to 30 keywords to describe your aid (separated '
                      'by ",")'),
        }
        for field, help_text in custom_help_text.items():
            if field in self.fields:
                self.fields[field].help_text = help_text

    def clean(self):
        """Custom validation routine."""

        data = self.cleaned_data

        if 'financers' in self.fields:
            if not any((data.get('financers'),
                        data.get('financer_suggestion'))):
                msg = _('Please provide a financer, or suggest a new one.')
                self.add_error('financers', msg)

        if 'subvention_rate' in data and data['subvention_rate']:
            lower = data['subvention_rate'].lower
            upper = data['subvention_rate'].upper
            if lower and not upper:
                msg = _('Please indicate the maximum subvention rate.')
                self.add_error(
                    'subvention_rate',
                    ValidationError(msg, code='missing_upper_bound'))

        return data

    def save(self, commit=True):
        """Saves the instance.

        We update the aid search_vector here, because this is the only place
        we gather all the necessary data (object + m2m related objects).
        """
        financers = self.cleaned_data.get('financers', None)
        instructors = self.cleaned_data.get('instructors', None)
        self.instance.set_search_vector(financers, instructors)
        return super().save(commit=commit)

    def _save_m2m(self):
        super()._save_m2m()
        self.instance.populate_tags()


class AidAdminForm(BaseAidForm):
    """Custom Aid edition admin form."""

    financer_suggestion = forms.CharField(
        label=_('Financer suggestion'),
        max_length=256,
        required=False,
        help_text=_('This financer was suggested. Add it to the global list '
                    'then add it to this aid with the field above.'))
    instructor_suggestion = forms.CharField(
        label=_('Instructor suggestion'),
        max_length=256,
        required=False,
        help_text=_('This instructor was suggested. Add it to the global list '
                    'then add it to this aid with the field above.'))
    categories = CategoryMultipleChoiceField(
        label=_('Categories'),
        required=False,
        widget=FilteredSelectMultiple(_('Categories'), True))

    class Meta:
        widgets = {
            'name': forms.Textarea(attrs={'rows': 3}),
            'mobilization_steps': forms.CheckboxSelectMultiple,
            'targeted_audiances': forms.CheckboxSelectMultiple,
            'aid_types': forms.CheckboxSelectMultiple,
            'destinations': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['financers'].required = False
        self.fields['tags'].widget.attrs['class'] = 'admin-autocomplete'


class AidEditForm(BaseAidForm):

    financers = forms.ModelMultipleChoiceField(
        label=_('Backers'),
        queryset=Backer.objects.all(),
        widget=AutocompleteSelectMultiple,
        required=False,
        help_text=_('Type a few characters and select a value among the list'))
    financer_suggestion = forms.CharField(
        label=_('Suggest a new financer'),
        max_length=256,
        required=False,
        help_text=_('Suggest a financer if you don\'t find '
                    'the correct choice in the main list.'))
    instructors = forms.ModelMultipleChoiceField(
        label=_('Backers'),
        queryset=Backer.objects.all(),
        widget=AutocompleteSelectMultiple,
        required=False,
        help_text=_('Type a few characters and select a value among the list'))
    instructor_suggestion = forms.CharField(
        label=_('Suggest a new instructor'),
        max_length=256,
        required=False,
        help_text=_('Suggest an instructor if you don\'t find '
                    'the correct choice in the main list.'))

    perimeter = PerimeterChoiceField(
        label=_('Perimeter'))

    class Meta:
        model = Aid
        fields = [
            'name',
            'description',
            'tags',
            'targeted_audiances',
            'financers',
            'financer_suggestion',
            'instructors',
            'instructor_suggestion',
            'recurrence',
            'start_date',
            'predeposit_date',
            'submission_deadline',
            'perimeter',
            'is_call_for_project',
            'aid_types',
            'subvention_rate',
            'subvention_comment',
            'mobilization_steps',
            'destinations',
            'eligibility',
            'origin_url',
            'application_url',
            'contact',
        ]
        widgets = {
            'mobilization_steps': MultipleChoiceFilterWidget,
            'destinations': MultipleChoiceFilterWidget,
            'targeted_audiances': MultipleChoiceFilterWidget,
            'aid_types': MultipleChoiceFilterWidget,
            'start_date': forms.TextInput(
                attrs={'type': 'date', 'placeholder': _('yyyy-mm-dd')}),
            'predeposit_date': forms.TextInput(
                attrs={'type': 'date', 'placeholder': _('yyyy-mm-dd')}),
            'submission_deadline': forms.TextInput(
                attrs={'type': 'date', 'placeholder': _('yyyy-mm-dd')})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'subvention_rate' in self.fields:
            range_widgets = self.fields['subvention_rate'].widget.widgets
            range_widgets[0].attrs['placeholder'] = _('Min. subvention rate')
            range_widgets[1].attrs['placeholder'] = _('Max. subvention rate')


class AidAmendForm(AidEditForm):
    amendment_author_name = forms.CharField(
        label=_('Who are you?'),
        widget=forms.TextInput(attrs={
            'maxlength': 256,
            'placeholder': _('Your full name')}),
        required=True,
        max_length=256)
    amendment_author_email = forms.EmailField(
        label=_('Your email address'),
        required=False,
        help_text=_('Leave us an address if you want a followup.'))
    amendment_author_org = forms.CharField(
        label=_('Your organization'),
        required=False,
        help_text=_('Help us understand who you are.'))
    amendment_comment = forms.CharField(
        label=_('Care to comment?'),
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False,
        help_text=_('If you want to pass additional details about your \
                     amendment, please tell us here.'))

    class Meta(AidEditForm.Meta):
        fields = AidEditForm.Meta.fields + [
            'amendment_author_name', 'amendment_author_email',
            'amendment_author_org', 'amendment_comment'
        ]


class AidSearchForm(forms.Form):
    """Main form for search engine."""

    AID_CATEGORY_CHOICES = (
        ('', ''),
        ('funding', _('Funding')),
        ('non-funding', _('Non-funding')),
    )

    ORDER_BY = (
        ('relevance', _('Sort: relevance')),
        ('publication_date', _('Sort: publication date')),
        ('submission_deadline', _('Sort: submission deadline')),
    )

    perimeter = PerimeterChoiceField(
        label=_('Your project\'s location'),
        required=False)
    text = forms.CharField(
        label=_('Text search'),
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Aid title, keyword, etc.')}))
    apply_before = forms.DateField(
        label=_('Apply before…'),
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date'}))
    financial_aids = forms.MultipleChoiceField(
        label=_('Financial aids'),
        required=False,
        choices=FINANCIAL_AIDS,
        widget=forms.CheckboxSelectMultiple)
    technical_aids = forms.MultipleChoiceField(
        label=_('Technical aids'),
        required=False,
        choices=TECHNICAL_AIDS,
        widget=forms.CheckboxSelectMultiple)
    mobilization_step = forms.MultipleChoiceField(
        label=_('Project progress'),
        required=False,
        choices=Aid.STEPS,
        widget=forms.CheckboxSelectMultiple)
    destinations = forms.MultipleChoiceField(
        label=_('Concerned actions'),
        required=False,
        choices=Aid.DESTINATIONS,
        widget=forms.CheckboxSelectMultiple)
    call_for_projects_only = forms.BooleanField(
        label=_('Call for projects only'),
        required=False)
    targeted_audiances = forms.MultipleChoiceField(
        label=_('I am…'),
        required=False,
        choices=Aid.AUDIANCES,
        widget=forms.CheckboxSelectMultiple)

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
        if not hasattr(self, 'cleaned_data'):
            self.full_clean()

        perimeter = self.cleaned_data.get('perimeter', None)
        if perimeter:
            qs = self.perimeter_filter(qs, perimeter)

        mobilization_steps = self.cleaned_data.get('mobilization_step', None)
        if mobilization_steps:
            qs = qs.filter(mobilization_steps__overlap=mobilization_steps)

        # Those two form fields are split for form readability,
        # but they relate to a single model field.
        financial_aids = self.cleaned_data.get('financial_aids', [])
        technical_aids = self.cleaned_data.get('technical_aids', [])
        aid_types = financial_aids + technical_aids
        if aid_types:
            qs = qs.filter(aid_types__overlap=aid_types)

        destinations = self.cleaned_data.get('destinations', None)
        if destinations:
            qs = qs.filter(destinations__overlap=destinations)

        apply_before = self.cleaned_data.get('apply_before', None)
        if apply_before:
            qs = qs.filter(submission_deadline__lt=apply_before)

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

        targeted_audiances = self.cleaned_data.get('targeted_audiances', None)
        if targeted_audiances:
            qs = qs.filter(targeted_audiances__overlap=targeted_audiances)

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
            order_fields = ['-date_published'] + order_fields
        elif manual_order == 'submission_deadline':
            order_fields = ['submission_deadline'] + order_fields

        qs = qs.order_by(*order_fields)
        return qs

    def perimeter_filter(self, qs, search_perimeter):
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

        q_exact_match = Q(perimeter=search_perimeter)
        q_contains = Q(perimeter__in=search_perimeter.contained_in.all())
        q_contained = Q(perimeter__contained_in=search_perimeter)
        qs = qs.filter(q_exact_match | q_contains | q_contained).distinct()

        return qs
