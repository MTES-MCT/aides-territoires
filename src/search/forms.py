from django import forms
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from core.forms import GroupedModelChoiceField
from categories.models import Theme, Category
from aids.models import Aid
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


class ThemeWidget(forms.widgets.ChoiceWidget):
    """Custom widget to select themes."""

    allow_multiple_selected = True
    template_name = 'search/forms/widgets/theme_widget.html'


class ThemeChoiceIterator(forms.models.ModelChoiceIterator):
    def choice(self, obj):
        return (
            obj['categories__theme__slug'],
            self.field.label_from_instance(obj),
        )


class ThemeChoiceField(forms.ModelMultipleChoiceField):

    iterator = ThemeChoiceIterator

    def label_from_instance(self, obj):
        return '{} ({})'.format(
            obj['categories__theme__name'], obj['nb_aids'])


class ThemeSearchForm(forms.Form):
    targeted_audiances = forms.CharField(
        widget=forms.widgets.HiddenInput)
    perimeter = forms.CharField(
        widget=forms.widgets.HiddenInput)
    theme = ThemeChoiceField(
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
        aids = Aid.objects \
            .published() \
            .open()
        filter_form = AidSearchForm(self.data)
        themes_with_aid_count = filter_form.filter_queryset(aids) \
            .values('categories__theme__slug', 'categories__theme__name') \
            .annotate(nb_aids=Count('id', distinct=True)) \
            .order_by('categories__theme__name')
        self.fields['theme'].queryset = themes_with_aid_count


class CategoryWidget(forms.widgets.ChoiceWidget):
    """Custom widget to select categories grouped by themes."""

    allow_multiple_selected = True
    template_name = 'search/forms/widgets/category_widget.html'


class CategorySearchForm(forms.Form):
    targeted_audiances = forms.CharField(
        widget=forms.widgets.HiddenInput)
    perimeter = forms.CharField(
        widget=forms.widgets.HiddenInput)
    theme = forms.ModelMultipleChoiceField(
        queryset=Theme.objects.all(),
        to_field_name='slug',
        widget=forms.widgets.MultipleHiddenInput)
    category = GroupedModelChoiceField(
        queryset=Category.objects.all(),
        choices_groupby='theme',
        empty_label=None,
        to_field_name='slug',
        widget=CategoryWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        themes = self['theme'].value()
        self.fields['category'].queryset = Category.objects \
            .filter(theme__slug__in=themes) \
            .select_related('theme') \
            .order_by('theme__name', 'name')
