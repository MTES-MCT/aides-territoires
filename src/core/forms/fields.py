from django import forms
from dataproviders.utils import content_prettify


class RichTextField(forms.CharField):
    """A text field with a rich text editor.

    This class does two main things:
      - add a css class to trigger the rich js text editor
      - sanitize the generated html
    """

    CSS_CLASS = 'textarea-wysiwyg'

    def __init__(self, *args, widget=None, **kwargs):
        widget = widget or forms.Textarea
        super().__init__(*args, widget=widget, **kwargs)

    def widget_attrs(self, widget):
        """Add a custom css class to the widget."""

        attrs = super().widget_attrs(widget)
        attrs.update({
            'class': self.CSS_CLASS
        })
        return attrs

    def clean(self, value):
        """Sanitize the html."""

        cleaned = super().clean(value)
        return content_prettify(cleaned, more_allowed_tags=['a'])
