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
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class PercentRangeField(IntegerRangeField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(validators.RangeMinValueValidator(0))
        self.validators.append(validators.RangeMaxValueValidator(100))
