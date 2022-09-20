from django import forms

from geofr.constants import REGIONS, DEPARTMENTS


class RegionField(forms.ChoiceField):
    """Form field to select a single french region."""

    def __init__(self, *args, **kwargs):

        kwargs["choices"] = REGIONS
        super().__init__(**kwargs)


class DepartmentField(forms.ChoiceField):
    """Form field to select a single french department."""

    def __init__(self, *args, **kwargs):

        kwargs["choices"] = DEPARTMENTS
        super().__init__(**kwargs)
