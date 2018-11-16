from django import forms


class AutocompleteMixin:
    """Common code for select widget designed to be used with select2.

    The main difference with default select widget is that we don't render
    the entire queryset as a huge <option> list.
    """

    def __init__(self, *args, **kwargs):
        self.choices = list()
        return super().__init__(*args, **kwargs)

    def optgroups(self, name, value, attr=None):
        """Return selected options based on the ModelChoiceIterator.

        Shamelessy stolen from Django admin's autocomplete widget.
        """

        default = (None, [], 0)
        groups = [default]
        has_selected = False
        selected_choices = {
            str(v) for v in value
            if str(v) not in self.choices.field.empty_values
        }
        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, '', '', False, 0))
        choices = (
            (obj.pk, self.choices.field.label_from_instance(obj))
            for obj in self.choices.queryset.filter(pk__in=selected_choices)
        )
        for option_value, option_label in choices:
            selected = (
                str(option_value) in value and
                (has_selected is False or self.allow_multiple_selected)
            )
            has_selected |= selected
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(self.create_option(
                name, option_value, option_label, selected_choices, index))
        return groups


class AutocompleteSelect(AutocompleteMixin, forms.Select):
    pass


class AutocompleteSelectMultiple(AutocompleteMixin, forms.SelectMultiple):
    pass


class MultipleChoiceFilterWidget(forms.widgets.CheckboxSelectMultiple):
    """A basic multi checkbox widget with a custom template.

    We can't override the default template because it would mess with the
    django admin.
    """

    template_name = 'forms/widgets/multiple_input.html'
