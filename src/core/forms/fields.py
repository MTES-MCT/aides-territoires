from functools import partial
from itertools import groupby
from operator import attrgetter
from django import forms

from core.forms.widgets import AutocompleteSelect, AutocompleteSelectMultiple
from dataproviders.utils import content_prettify


class RichTextField(forms.CharField):
    """A text field with a rich text editor.

    This class does two main things:
      - add a css class to trigger the rich js text editor
      - sanitize the generated html
    """

    CSS_CLASS = "textarea-wysiwyg"

    def __init__(self, *args, widget=None, **kwargs):
        widget = widget or forms.Textarea
        super().__init__(*args, widget=widget, **kwargs)

    def widget_attrs(self, widget):
        """Add a custom css class to the widget."""

        attrs = super().widget_attrs(widget)
        attrs.update({"class": self.CSS_CLASS})
        return attrs

    def clean(self, value):
        """Sanitize the html."""

        cleaned = super().clean(value)
        extra_tags = ["a", "blockquote", "br", "header", "footer", "img"]
        extra_attrs = ["style"]
        return content_prettify(
            cleaned,
            more_allowed_tags=extra_tags,
            more_allowed_attrs=extra_attrs,
        ).strip()


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
            msg = (
                "choices_groupby must either be a str or a callable "
                "accepting a single argument"
            )
            raise TypeError(msg)
        self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
        super().__init__(*args, **kwargs)


class AutocompleteModelChoiceField(forms.ModelChoiceField):
    """A custom fields that works well with autocomplete widgets.

    In the aid search form, fields are submitted as "GET" values and thus they
    appear in the url.

    For this reason, we draft custom `id` values in the form "{id}-{slug}" so
    the search filter url stays readable.

    This field's job is to get rid of the "-{slug}" part when it performs its
    usal field tasks.
    """

    def __init__(self, *args, widget=None, **kwargs):
        if widget is None:
            widget = AutocompleteSelect

        super().__init__(*args, widget=widget, **kwargs)

    def to_python(self, value):
        value = self.prepare_value(value)
        return super().to_python(value)

    def prepare_value(self, value):
        if isinstance(value, str):
            value = value.split("-")[0]
        return value


class AutocompleteModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """A custom field that works well with autocomplete widgets.

    See `AutocompleteModelChoiceField.`
    """

    def __init__(self, *args, widget=None, **kwargs):
        if widget is None:
            widget = AutocompleteSelectMultiple

        super().__init__(*args, widget=widget, **kwargs)

    def to_python(self, value):
        value = self.prepare_value(value)
        return super().to_python(value)

    def prepare_value(self, value):
        def clean_val(val):
            if isinstance(val, str):
                val = val.split("-")[0]
            return val

        if (
            hasattr(value, "__iter__")
            and not isinstance(value, str)
            and not hasattr(value, "_meta")
        ):
            value = [clean_val(val) for val in value]

        return super().prepare_value(value)
