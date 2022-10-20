from django import forms
from django.contrib.postgres.fields import ArrayField, IntegerRangeField
from django.contrib.postgres import validators


class ChoiceArrayField(ArrayField):
    """Custom ArrayField with a ChoiceField as default field.

    The default field is a comma-separated InputText, which is not very
    usefull.

    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class RangeMinValueOrNoneValidator(validators.RangeMinValueValidator):
    """Make sure the lower range is > some value *if* it is provided."""

    def compare(self, a, b):
        return a.lower is not None and a.lower < b


class RangeMaxValueOrNoneValidator(validators.RangeMaxValueValidator):
    """Make sure the upper range is < some value *if* it is provided."""

    def compare(self, a, b):
        return a.upper is not None and a.upper > b


class PercentRangeField(IntegerRangeField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(RangeMinValueOrNoneValidator(0))
        self.validators.append(RangeMaxValueOrNoneValidator(100))
