from django import forms
from django.utils.text import slugify


class TagChoiceField(forms.MultipleChoiceField):
    """Custom form field for tags."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['class'] = 'tag-field'

    def valid_value(self, valid_value):
        """Unexisting tags will be created. Hence, all values are valid."""
        return True

    def to_python(self, value):
        """All tags must be represented as slugs."""
        list_value = super().to_python(value)
        return [slugify(value, allow_unicode=True) for value in list_value]
