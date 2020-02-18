from functools import partial
from itertools import groupby
from operator import attrgetter
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
        return content_prettify(cleaned, more_allowed_tags=['a']).strip()


class GroupedModelChoiceIterator(forms.models.ModelChoiceIterator):
    def __init__(self, field, groupby):
        self.groupby = groupby
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset
        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, objs in groupby(queryset, self.groupby):
            yield (group, [self.choice(obj) for obj in objs])


class GroupedModelChoiceField(forms.ModelChoiceField):
    """A model choice field with the ability to generate optgroups.

    Shamelessly stolen from here:
    https://code.djangoproject.com/ticket/27331#comment:7
    """
    def __init__(self, *args, choices_groupby, **kwargs):
        if isinstance(choices_groupby, str):
            choices_groupby = attrgetter(choices_groupby)
        elif not callable(choices_groupby):
            msg = 'choices_groupby must either be a str or a callable ' \
                  'accepting a single argument'
            raise TypeError(msg)
        self.iterator = partial(
            GroupedModelChoiceIterator, groupby=choices_groupby)
        super().__init__(*args, **kwargs)
