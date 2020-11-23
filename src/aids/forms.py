import re
import operator

from django import forms
from django.db.models import Q, F
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.postgres.search import SearchQuery, SearchRank

from core.forms import (
    AutocompleteModelChoiceField, AutocompleteModelMultipleChoiceField,
    MultipleChoiceFilterWidget, RichTextField)
from geofr.models import Perimeter
from geofr.utils import search_perimeter_by_id
from backers.models import Backer
from categories.fields import CategoryMultipleChoiceField
from categories.models import Category, Theme
from programs.models import Program
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

COLLECTIVITIES_AUDIENCES = (
    ('commune', _('Communes')),
    ('epci', _('Audience EPCI')),
    ('department', _('Departments')),
    ('region', _('Regions')),
)

OTHER_AUDIENCES = (
    ('association', _('Associations')),
    ('private_person', _('Individuals')),
    ('farmer', _('Farmers')),
    ('private_sector', _('Private sector')),
    ('public_cies', _('Local public companies')),
    ('public_org', _('Public organizations / State services')),
    ('researcher', _('Research')),
)

AUDIENCES = (
    (_('Collectivities'), COLLECTIVITIES_AUDIENCES),
    (_('Other audiences'), OTHER_AUDIENCES)
)

IS_CALL_FOR_PROJECT = (
    (None, '----'),
    (True, _('Yes')),
    (False, _('No'))
)


class BaseAidForm(forms.ModelForm):
    """Base for all aid edition forms (front, admin, amendments)."""

    short_title = forms.CharField(
        label=_('Program title'),
        required=False,
        max_length=64,
        widget=forms.TextInput(
            attrs={'placeholder': _('Call for project "Innovation continue"')}
        ))
    description = RichTextField(
        label=_('Full description of the aid and its objectives'),
        widget=forms.Textarea(attrs={'placeholder': _(
            'If you have a description, do not hesitate to copy it here.\n'
            'Try to complete the description with the maximum of'
            ' information.\n'
            'If you are contacted regularly to ask for the same information,'
            ' try to give some answers in this space.')}))
    project_examples = RichTextField(
        label=_('Examples of projects that benefited from this aid'),
        required=False,
        help_text=_(
            'Give concrete examples of projets that benefited or might '
            'benefit from this aid.'),
        widget=forms.Textarea(attrs={'placeholder': _(
            'Library, skatepark, etc.')}))
    eligibility = RichTextField(
        label=_('Other eligibility criterias?'),
        required=False)
    contact = RichTextField(
        label=_('Contact to apply'),
        required=True,
        help_text=_('Feel free to add several contacts'),
        widget=forms.Textarea(attrs={'placeholder': _(
            'First name / last name, email, phone, comments…'
        )}))
    is_call_for_project = forms.BooleanField(
        label=_('Call for project / Call for expressions of interest'),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'aid_types' in self.fields:
            self.fields['aid_types'].choices = AID_TYPES

        if 'targeted_audiences' in self.fields:
            self.fields['targeted_audiences'].choices = AUDIENCES

        if 'recurrence' in self.fields:
            self.fields['recurrence'].required = True

        custom_labels = {
            'name': _('Aid title'),
            'financers': _('Aid backer(s)'),
            'instructors': _('Aid instructor(s)'),
            'new_backer': _('…or add a new financer'),
            'destinations': _('Types of expenses covered'),
            'origin_url': _('Link to a full description'),
            'application_url': _('Link to an online application form'),
            'is_call_for_project': _('Check this if this aid is a call for'
                                     ' project')
        }
        for field, label in custom_labels.items():
            if field in self.fields:
                self.fields[field].label = label

        custom_help_text = {
            'new_backer':
                _('If the aid backer is not in the previous list, use this '
                  'field to add a new one.'),
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


class AidAdminForm(BaseAidForm):
    """Custom Aid edition admin form."""

    perimeter_suggestion = forms.CharField(
        label=_('Perimeter suggestion'),
        max_length=256,
        required=False,
        help_text=_('The user suggested the following description for a new '
                    'perimeter'))

    financer_suggestion = forms.CharField(
        label=_('Backer suggestion'),
        max_length=256,
        required=False,
        help_text=_('This backer was suggested. Add it to the global list '
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
            'targeted_audiences': forms.CheckboxSelectMultiple,
            'aid_types': forms.CheckboxSelectMultiple,
            'destinations': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['financers'].required = False
        self.fields['start_date'].required = False


class AidEditForm(BaseAidForm):

    programs = forms.ModelMultipleChoiceField(
        label=_('Aid program'),
        queryset=Program.objects.all(),
        required=False)
    financers = AutocompleteModelMultipleChoiceField(
        label=_('Backers'),
        queryset=Backer.objects.all(),
        required=False,
        help_text=_('Type a few characters and select a value among the list'))
    financer_suggestion = forms.CharField(
        label=_('Suggest a new backer'),
        max_length=256,
        required=False,
        help_text=_('Suggest a backer if you don\'t find '
                    'the correct choice in the main list.'))
    instructors = AutocompleteModelMultipleChoiceField(
        label=_('Backers'),
        queryset=Backer.objects.all(),
        required=False,
        help_text=_('Type a few characters and select a value among the list'))
    instructor_suggestion = forms.CharField(
        label=_('Suggest a new instructor'),
        max_length=256,
        required=False,
        help_text=_('Suggest an instructor if you don\'t find '
                    'the correct choice in the main list.'))

    perimeter = AutocompleteModelChoiceField(
        queryset=Perimeter.objects.all(),
        label=_('Targeted area'),
        help_text=_('''
            The geographical zone where the aid is available.<br />
            Example of valid zones:
            <ul>
            <li>France</li>
            <li>Bretagne (Région)</li>
            <li>Métropole du Grand Paris (EPCI)</li>
            <li>Y (Commune)</li>
            <li>Outre-mer</li>
            <li>Wallis et Futuna</li>
            <li>Massif Central</li>
            <li>Action Cœur de Ville 2019</li>
            </ul>
        '''))
    perimeter_suggestion = forms.CharField(
        label=_('Can\'t find a valid targeted area?'),
        max_length=256,
        required=False,
        help_text=_('''
            If you can't find a corresponding targeted area amongst the
            existing perimeter list, just choose "France" and briefly describe
            here your aid actual target area.
        '''))
    categories = CategoryMultipleChoiceField(
        label=_('Aid categories'),
        help_text=_('Choose one or several categories that match your aid.'),
        required=False)

    class Meta:
        model = Aid
        fields = [
            'name',
            'short_title',
            'description',
            'categories',
            'project_examples',
            'targeted_audiences',
            'financers',
            'financer_suggestion',
            'instructors',
            'instructor_suggestion',
            'in_france_relance',
            'recurrence',
            'start_date',
            'predeposit_date',
            'submission_deadline',
            'perimeter',
            'perimeter_suggestion',
            'is_call_for_project',
            'programs',
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
            'targeted_audiences': MultipleChoiceFilterWidget,
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
        self.fields['mobilization_steps'].required = True

    def clean(self):
        """Validation routine (frontend form only)."""

        data = super().clean()
        if 'recurrence' in data and data['recurrence']:
            recurrence = data['recurrence']
            submission_deadline = data.get('submission_deadline', None)

            if recurrence != 'ongoing' and not submission_deadline:
                msg = _('Unless the aid is ongoing, you must indicate the submission deadline.')  # noqa
                self.add_error(
                    'submission_deadline',
                    ValidationError(msg, code='missing_submission_deadline'))

        return data


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


class BaseAidSearchForm(forms.Form):
    """Main form for search engine."""

    AID_CATEGORY_CHOICES = (
        ('', ''),
        ('funding', _('Funding')),
        ('non-funding', _('Non-funding')),
    )

    AID_TYPE_CHOICES = (
        ('financial', _('Financial aid')),
        ('technical', _('Engineering aid')),
    )

    ORDER_BY = (
        ('relevance', _('Sort: relevance')),
        ('publication_date', _('Sort: publication date')),
        ('submission_deadline', _('Sort: submission deadline')),
    )

    CATEGORIES_QS = Category.objects \
        .select_related('theme') \
        .order_by('theme__name', 'name')

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
    published_after = forms.DateField(
        label=_('Published after…'),
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date'}))
    aid_type = forms.MultipleChoiceField(
        label=_('Aid type'),
        choices=AID_TYPE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple)
    financial_aids = forms.MultipleChoiceField(
        label=_('Financial aids'),
        required=False,
        choices=FINANCIAL_AIDS,
        widget=forms.CheckboxSelectMultiple)
    technical_aids = forms.MultipleChoiceField(
        label=_('Engineering aids'),
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
    recurrence = forms.ChoiceField(
        label=_('Recurrence'),
        required=False,
        choices=Aid.RECURRENCE)
    call_for_projects_only = forms.BooleanField(
        label=_('Call for projects only'),
        required=False)
    backers = AutocompleteModelMultipleChoiceField(
        label=_('Backers'),
        queryset=Backer.objects.all(),
        required=False)
    programs = forms.ModelMultipleChoiceField(
        label=_('Aid programs'),
        queryset=Program.objects.all(),
        to_field_name='slug',
        required=False)
    in_france_relance = forms.BooleanField(
        label=_('France Relance?'),
        required=False)
    themes = forms.ModelMultipleChoiceField(
        label=_('Themes'),
        queryset=Theme.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.MultipleHiddenInput)
    categories = CategoryMultipleChoiceField(
        label=_('Themes'),  # Not a mistake
        queryset=CATEGORIES_QS,
        to_field_name='slug',
        required=False)
    targeted_audiences = forms.MultipleChoiceField(
        label=_('You are seeking aids for…'),
        required=False,
        choices=Aid.AUDIENCES,
        widget=forms.CheckboxSelectMultiple)
    perimeter = AutocompleteModelChoiceField(
        queryset=Perimeter.objects.all(),
        label=_('Your territory'),
        required=False)

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

    def filter_queryset(self, qs=None):
        """Filter querysets depending of input data."""

        # If no qs was passed, just start with all published aids
        if qs is None:
            qs = Aid.objects.published().open()

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

        aid_type = self.cleaned_data['aid_type']
        if 'financial' in aid_type:
            aid_types += Aid.FINANCIAL_AIDS
        if 'technical' in aid_type:
            aid_types += Aid.TECHNICAL_AIDS

        if aid_types:
            qs = qs.filter(aid_types__overlap=aid_types)

        destinations = self.cleaned_data.get('destinations', None)
        if destinations:
            qs = qs.filter(destinations__overlap=destinations)

        apply_before = self.cleaned_data.get('apply_before', None)
        if apply_before:
            qs = qs.filter(submission_deadline__lte=apply_before)

        published_after = self.cleaned_data.get('published_after', None)
        if published_after:
            qs = qs.filter(date_published__gte=published_after)

        recurrence = self.cleaned_data.get('recurrence', None)
        if recurrence:
            qs = qs.filter(recurrence=recurrence)

        call_for_projects_only = self.cleaned_data.get(
            'call_for_projects_only', False)
        if call_for_projects_only:
            qs = qs.filter(is_call_for_project=True)

        in_france_relance = self.cleaned_data.get('in_france_relance', False)
        if in_france_relance:
            qs = qs.filter(in_france_relance=True)

        text = self.cleaned_data.get('text', None)
        if text:
            query = self.parse_query(text)
            qs = qs \
                .filter(search_vector=query) \
                .annotate(rank=SearchRank(F('search_vector'), query))

        targeted_audiences = self.cleaned_data.get('targeted_audiences', None)
        if targeted_audiences:
            qs = qs.filter(targeted_audiences__overlap=targeted_audiences)

        categories = self.cleaned_data.get('categories', None)
        if categories:
            qs = qs.filter(categories__in=categories)

        programs = self.cleaned_data.get('programs', None)
        if programs:
            qs = qs.filter(programs__in=programs)

        # We filter by theme only if no categories were provided.
        # This is to handle the following edge case: on the multi-step search
        # form, the user selects a theme, then on the last step, doesn't select
        # any categories and just click "Search".
        themes = self.cleaned_data.get('themes', None)
        if themes and not categories:
            qs = qs.filter(categories__theme__in=themes)

        backers = self.cleaned_data.get('backers', None)
        if backers:
            qs = qs.filter(
                Q(financers__in=backers) | Q(instructors__in=backers))

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

    def get_order_fields(self, qs):
        """On which fields must this queryset be sorted?."""

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

        return order_fields

    def order_queryset(self, qs):
        """Set the order value on the queryset."""
        qs = qs.order_by(*self.get_order_fields(qs))
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
        perimeter_qs = search_perimeter_by_id(search_perimeter.id)
        qs = qs.filter(perimeter__in=perimeter_qs)
        return qs


class AidSearchForm(BaseAidSearchForm):
    """The main search result filter form."""

    targeted_audiences = forms.MultipleChoiceField(
        label=_('The structure'),
        required=False,
        choices=Aid.AUDIENCES)


class AdvancedAidFilterForm(BaseAidSearchForm):
    """An "advanced" aid list filter form with more criterias."""

    targeted_audiences = forms.MultipleChoiceField(
        label=_('You are seeking aids for…'),
        required=False,
        choices=Aid.AUDIENCES,
        widget=forms.CheckboxSelectMultiple)
