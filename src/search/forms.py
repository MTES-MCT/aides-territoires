from itertools import groupby
from operator import itemgetter

from django import forms
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from categories.models import Theme, Category
from aids.forms import AidSearchForm
from geofr.forms.fields import PerimeterChoiceField


AUDIANCES = [
    (_('A collectivity'), (
        ('commune', _('Commune')),
        ('department', _('Department')),
        ('region', _('Region')),
    )),
    (_('An other beneficiary'), (
        ('public_org', _('Public organizations')),
        ('association', _('Associations')),
    ))
]


class AudianceWidget(forms.widgets.ChoiceWidget):
    """Custom widget for the audiance search step."""

    allow_multiple_selected = False
    template_name = 'search/forms/widgets/audiance_widget.html'


class AudianceSearchForm(forms.Form):
    targeted_audiances = forms.ChoiceField(
        label=_('Your are seeking aids for…'),
        required=False,
        choices=AUDIANCES,
        widget=AudianceWidget)


class PerimeterSearchForm(forms.Form):
    targeted_audiances = forms.CharField(
        widget=forms.widgets.HiddenInput)
    perimeter = PerimeterChoiceField(
        label=_('Your territory'),
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
        return '{} ({})'.format(
            obj['categories__theme__name'], obj['nb_aids'])


class ThemeWidget(forms.widgets.ChoiceWidget):
    """Custom widget to select themes."""

    allow_multiple_selected = True
    template_name = 'search/forms/widgets/theme_widget.html'


class ThemeSearchForm(forms.Form):
    targeted_audiances = forms.CharField(
        widget=forms.widgets.HiddenInput)
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
            .values('categories__theme__slug', 'categories__theme__name') \
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
    targeted_audiances = forms.CharField(
        widget=forms.widgets.HiddenInput)
    perimeter = forms.CharField(
        widget=forms.widgets.HiddenInput)
    # Note: we don't add a field for themes, because we don't want
    # that value to be passed to the following search form
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
