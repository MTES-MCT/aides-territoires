from itertools import groupby
from operator import itemgetter

from django import forms
from django.db.models import Count
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.core.exceptions import ValidationError

from core.forms.fields import RichTextField, AutocompleteModelChoiceField
from categories.models import Theme, Category
from projects.models import Project
from categories.fields import CategoryMultipleChoiceField
from geofr.models import Perimeter
from aids.forms import AidSearchForm


AUDIENCES = [
    ('Une collectivité', (
        ('commune', 'Commune'),
        ('epci', 'Intercommunalité / Pays'),
        ('department', 'Département'),
        ('region', 'Région'),
        ('special', 'Statut particulier'),
    )),
    ('Un autre bénéficiaire', (
        ('public_org', 'Établissement public'),
        ('association', 'Association'),
        ('private_sector', 'Entreprise privée'),
        ('farmer', 'Agriculteur'),
    ))
]


class AudienceWidget(forms.widgets.ChoiceWidget):
    """Custom widget for the audience search step."""

    allow_multiple_selected = False
    template_name = 'search/forms/widgets/audience_widget.html'


class AudienceSearchForm(forms.Form):
    targeted_audiences = forms.MultipleChoiceField(
        label=_('Your are seeking aids for…'),
        required=False,
        choices=AUDIENCES,
        widget=AudienceWidget)


class PerimeterSearchForm(forms.Form):
    targeted_audiences = forms.MultipleChoiceField(
        widget=forms.widgets.MultipleHiddenInput)
    perimeter = AutocompleteModelChoiceField(
        label=_('Your territory'),
        queryset=Perimeter.objects.all(),
        required=False)


class ThemeChoiceIterator(forms.models.ModelChoiceIterator):
    """Custom iterator for the `Theme` queryset.

    This class generates the list of choices to be rendered by the widget.

    We need to create a custom iterator because the theme queryset is
    a bit peculiar. See below.
    """
    def choice(self, obj):
        return (
            obj['categories__theme__slug'],
            self.field.label_from_instance(obj),
        )


class ThemeChoiceField(forms.ModelMultipleChoiceField):
    """Custom choice field to select Themes.

    We override the iterator and display the number of matching aids
    in the widget.
    """
    iterator = ThemeChoiceIterator

    def label_from_instance(self, obj):
        return format_html(
                    '{theme_name} ({nb_aids})'
                    '<span>{theme_short_description}</span>',
                    theme_name=obj['categories__theme__name'],
                    nb_aids=obj['nb_aids'],
                    theme_short_description=obj['categories__theme__short_description'], # noqa
                )


class ThemeWidget(forms.widgets.ChoiceWidget):
    """Custom widget to select themes."""

    allow_multiple_selected = True
    template_name = 'search/forms/widgets/theme_widget.html'


class ThemeSearchForm(forms.Form):
    targeted_audiences = forms.MultipleChoiceField(
        choices=AUDIENCES,
        widget=forms.widgets.MultipleHiddenInput)
    perimeter = forms.CharField(
        widget=forms.widgets.HiddenInput)
    themes = ThemeChoiceField(
        queryset=Theme.objects.order_by('name'),
        to_field_name='slug',
        widget=ThemeWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # We have a problem here.
        # We want to return the list of existing themes, but we also want to
        # count the number of aids **matching the current search** for each
        # theme.
        #
        # Since the search query is already quite complex to generate, we
        # use it as a base and then we do a join on categories and themes,
        # then we group by theme and count.
        filter_form = AidSearchForm(self.initial)
        themes_with_aid_count = filter_form.filter_queryset() \
            .exclude(categories__isnull=True) \
            .values('categories__theme__slug',
                    'categories__theme__name',
                    'categories__theme__short_description') \
            .annotate(nb_aids=Count('id', distinct=True)) \
            .order_by('categories__theme__name')
        self.fields['themes'].queryset = themes_with_aid_count


class CategoryIterator(forms.models.ModelChoiceIterator):
    """Custom iterator for the category list.

    We do several custom things here:
      - handle the peculiar queryset that was used to select categories
      - group the categories by the associated theme
      - pass the correct parameters to the widget renderer.
    """
    groupby = 'categories__theme__name'  # as selected in the queryset

    def __iter__(self):

        for group, objs in groupby(self.queryset, itemgetter(self.groupby)):
            yield (group, [self.choice(obj) for obj in objs])

    def choice(self, obj):
        return (
            obj['categories__slug'],
            self.field.label_from_instance(obj),
        )


class CategoryChoiceField(forms.ModelMultipleChoiceField):
    """Custom choice field for the category list.

    We override the iterator and pass the aid count to the widget label.
    """
    iterator = CategoryIterator

    def label_from_instance(self, obj):
        return '{} ({})'.format(
            obj['categories__name'], obj['nb_aids'])


class CategoryWidget(forms.widgets.ChoiceWidget):
    """Custom widget to select categories grouped by themes."""

    allow_multiple_selected = True
    template_name = 'search/forms/widgets/category_widget.html'


class CategorySearchForm(forms.Form):
    targeted_audiences = forms.MultipleChoiceField(
        choices=AUDIENCES,
        widget=forms.widgets.MultipleHiddenInput)
    perimeter = forms.CharField(
        widget=forms.widgets.HiddenInput)
    themes = ThemeChoiceField(
        queryset=Theme.objects.order_by('name'),
        to_field_name='slug',
        widget=forms.widgets.MultipleHiddenInput)
    categories = CategoryChoiceField(
        queryset=Category.objects.all(),
        to_field_name='slug',
        widget=CategoryWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # See `ThemeSearchForm` for explanation about the following lines.
        filter_form = AidSearchForm(self.initial)
        filtered_qs = filter_form.filter_queryset() \
            .exclude(categories__isnull=True)

        # We list categories for selected themes
        # Special case: if no theme was selected, we return all of them
        themes = self.initial.get('themes', [])
        if themes:
            filtered_qs = filtered_qs \
                .filter(categories__theme__slug__in=themes)

        categories_with_aid_count = filtered_qs \
            .values(
                'categories__theme__name',
                'categories__name',
                'categories__slug') \
            .annotate(nb_aids=Count('id', distinct=True)) \
            .order_by('categories__theme__name', 'categories__name')
        self.fields['categories'].queryset = categories_with_aid_count


class ProjectSearchForm(forms.Form):
    targeted_audiences = forms.MultipleChoiceField(
        choices=AUDIENCES,
        widget=forms.widgets.MultipleHiddenInput)
    perimeter = forms.CharField(
        widget=forms.widgets.HiddenInput)
    themes = ThemeChoiceField(
        queryset=Theme.objects.order_by('name'),
        to_field_name='slug',
        widget=forms.widgets.MultipleHiddenInput)
    categories = CategoryChoiceField(
        queryset=Category.objects.all(),
        to_field_name='slug',
        widget=forms.widgets.MultipleHiddenInput)
    projects = AutocompleteModelChoiceField(
        queryset=Project.objects.all(),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        categories = self.initial.get('categories', [])

        category_id = Category.objects \
            .filter(slug__in=categories) \
            .values('id') \
            .distinct()

        self.fields['projects'].queryset = Project.objects \
            .filter(status='published') \
            .filter(categories__in=category_id) \
            .distinct()


class SearchPageAdminForm(forms.ModelForm):
    content = RichTextField(
        label=_('Page content'),
        help_text=_('Full description of the page. '
                    'Will be displayed above results.'))
    more_content = RichTextField(
        label=_('More content'),
        help_text=_('Hidden content, only revealed on a `See more` click.'))
    available_categories = CategoryMultipleChoiceField(
        label=_('Categories'),
        required=False,
        widget=FilteredSelectMultiple(_('Categories'), True))

    def clean(self):
        """Validate search page customization consistency.

        Filters consistency: we need to make sure that at least one
        search form field is selected.

        """
        data = super().clean()

        search_fields = [
            'show_perimeter_field', 'show_audience_field',
            'show_categories_field', 'show_mobilization_step_field',
            'show_aid_type_field', 'show_backers_field',
        ]
        nb_filters = 0
        for field in search_fields:
            if field in data and data[field]:
                nb_filters += 1

        if nb_filters == 0:
            raise ValidationError(
                _('You need to select at least one search form filter.'),
                code='not_enough_filters')

        if nb_filters > 3:
            raise ValidationError(
                _('You need to select less than four search form filters.'),
                code='too_many_filters')

        return data
