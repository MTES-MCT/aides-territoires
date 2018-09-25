from django import forms

from core.forms.widgets import AutocompleteSelect
from geofr.constants import REGIONS, DEPARTMENTS
from geofr.models import Perimeter


class RegionField(forms.ChoiceField):
    """Form field to select a single french region."""

    def __init__(self, *args, **kwargs):

        kwargs['choices'] = REGIONS
        super().__init__(**kwargs)


class DepartmentField(forms.ChoiceField):
    """Form field to select a single french department."""

    def __init__(self, *args, **kwargs):

        kwargs['choices'] = DEPARTMENTS
        super().__init__(**kwargs)


class PerimeterChoiceField(forms.ModelChoiceField):
    """Perimeter selection form field.

    Custom field to work with an autocomplete widget.
    """
    def __init__(self, *args, widget=None, **kwargs):  # noqa
        queryset = Perimeter.objects.all()
        if widget is None:
            widget = AutocompleteSelect

        return super().__init__(queryset, *args, widget=widget, **kwargs)

    def to_python(self, value):
        value = self.prepare_value(value)
        return super().to_python(value)

    def prepare_value(self, value):
        if isinstance(value, str):
            value = value.split('-')[0]
        return value
