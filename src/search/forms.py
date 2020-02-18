from django import forms
from django.utils.translation import ugettext_lazy as _

from core.forms import GroupedModelChoiceField
from categories.models import Theme, Category
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


class ThemeSearchForm(forms.Form):
    targeted_audiances = forms.CharField(
        widget=forms.widgets.HiddenInput)
    perimeter = forms.CharField(
        widget=forms.widgets.HiddenInput)
    theme = forms.ModelMultipleChoiceField(
        queryset=Theme.objects.order_by('name'),
        to_field_name='slug',
        widget=ThemeWidget)


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
