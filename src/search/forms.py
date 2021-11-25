from itertools import groupby
from operator import itemgetter

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils.html import format_html
from django.utils.text import slugify

from aids.forms import AidSearchForm
from categories.fields import CategoryMultipleChoiceField
from categories.models import Theme, Category
from core.forms.fields import RichTextField, AutocompleteModelChoiceField
from geofr.models import Perimeter
from pages.admin import PageForm


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
        label='La structure pour laquelle vous recherchez des aides est…',
        required=False,
        choices=AUDIENCES,
        widget=AudienceWidget)


class PerimeterSearchForm(forms.Form):
    targeted_audiences = forms.MultipleChoiceField(
        widget=forms.widgets.MultipleHiddenInput)
    perimeter = AutocompleteModelChoiceField(
        label='Votre territoire',
        queryset=Perimeter.objects.all(),
        required=False)


class ThemeChoiceIterator(forms.models.ModelChoiceIterator):
    """Custom iterator for the `Theme` queryset.

    This class generates the list of choices to be rendered by the widget.

    We need to create a custom iterator because the theme queryset is
    a bit peculiar. See below.
    """
    def choice(self, obj):
        return (obj['categories__theme__slug'], self.field.label_from_instance(obj))


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
            theme_short_description=obj['categories__theme__short_description']
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
    text = forms.CharField(
        label='Recherche textuelle',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Titre, sujet, mot-clé, etc.'}))

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
        return (obj['categories__slug'], self.field.label_from_instance(obj))


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


class SearchPageAdminForm(forms.ModelForm):
    content = RichTextField(
        label='Contenu de la page',
        help_text='Description complète de la page. Sera affichée au dessus des résultats.')
    more_content = RichTextField(
        label='Contenu additionnel',
        help_text='Contenu caché, révélé au clic sur le bouton « Voir plus ».')
    available_categories = CategoryMultipleChoiceField(
        label='Sous-thématiques',
        required=False,
        widget=FilteredSelectMultiple('Sous-thématiques', True))

    def clean(self):
        """Validate search page customization consistency.

        Filters consistency: we need to make sure that at least one
        search form field is selected.

        """
        data = super().clean()

        search_fields = [
            'show_perimeter_field', 'show_audience_field',
            'show_categories_field', 'show_mobilization_step_field',
            'show_aid_type_field', 'show_backers_field', 'show_text_field',
        ]

        # If there is no form customization fields, then we don't
        # need to run the fields validation. That's tipically the case
        # for lite admin page available to contributors that don't have
        # access to form customization.
        all_form_fields = self.fields.keys()
        has_form_customization_fields = any(
            field in all_form_fields for field in search_fields)
        if not has_form_customization_fields:
            return data

        nb_filters = 0
        for field in search_fields:
            if field in data and data[field]:
                nb_filters += 1

        if nb_filters == 0:
            raise ValidationError(
                'Vous devez sélectionner au moins un filtre pour le formulaire de recherche.',
                code='not_enough_filters')

        if nb_filters > 3:
            raise ValidationError(
                'Vous ne devez pas sélectionner plus de trois filtres pour le formulaire de recherche.',  # noqa
                code='too_many_filters')

        return data


class MinisiteTabForm(PageForm):
    pass


class MinisiteTabFormLite(MinisiteTabForm):
    url = forms.CharField(required=False)

    def build_url_from_title(self, title):
        slug = slugify(title)[:50]
        url = f'/{slug}/'
        return url

    def clean_url(self):
        url = self.cleaned_data['url']
        if not url:
            title = self.cleaned_data.get('title')
            url = self.build_url_from_title(title)
        return url

    def save(self, commit=True):
        if not self.instance.id:
            self.instance.url = self.cleaned_data['url']
        return super().save(commit=commit)
