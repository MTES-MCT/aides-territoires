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
            str(v) for v in value if str(v) not in self.choices.field.empty_values
        }

        # Prevent a bug when a user submits an invalid perimeter value,
        # e.g not an integer.
        #
        # Honestly, this problem should be handled on a higher level, by the
        # Field instance, but for some reason it isn't and I already spent
        # a few hours on this, so I decided to go for a somewhat quick
        # fix here.
        int_choices = set()
        for choice in selected_choices:
            try:
                val = int(choice)
                int_choices |= {val}
            except ValueError:
                pass
        selected_choices = int_choices

        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, "", "", False, 0))
        choices = (
            (obj.pk, self.choices.field.label_from_instance(obj))
            for obj in self.choices.queryset.filter(pk__in=selected_choices)
        )
        for option_value, option_label in choices:
            selected = str(option_value) in value and (
                has_selected is False or self.allow_multiple_selected
            )
            has_selected |= selected
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(
                self.create_option(
                    name, option_value, option_label, selected_choices, index
                )
            )
        return groups


class AutocompleteSelect(AutocompleteMixin, forms.Select):
    pass


class AutocompleteSelectSynonym(forms.Select):
    """
    For SynonymList a custom autocompleteselect is needed:
    This autocompleteselect allow to :
        - select new option without creating a corresponding object
        - select an option corresponding to an existing object
        - retrieve the selected option when we reload the page
    """

    def optgroups(self, name, value, attr=None):
        # Return selected option based on the ModelChoiceIterator.

        default = (None, [], 0)
        groups = [default]
        has_selected = False
        selected_choices = {
            str(v) for v in value if str(v) not in self.choices.field.empty_values
        }

        int_choices = set()
        for choice in selected_choices:
            try:
                val = int(choice)
                int_choices |= {val}
            except ValueError:
                pass
        selected_choices = int_choices

        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, "", "", False, 0))
            choices = (
                (
                    obj.id_slug,
                    self.choices.field.label_from_instance(obj.autocomplete_name),
                )
                for obj in self.choices.queryset.filter(pk__in=selected_choices)
            )

        if self.choices.queryset.filter(pk__in=selected_choices):
            for option_value, option_label in choices:
                selected = str(option_value) in value and (
                    has_selected is False or self.allow_multiple_selected
                )
                has_selected |= selected
                index = len(default[1])
                subgroup = default[1]
                subgroup.append(
                    self.create_option(
                        name, option_value, option_label, selected_choices, index
                    )
                )
        elif value != [""]:
            value = " ".join(value)
            selected = value
            has_selected = True
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(self.create_option(name, value, value, value, index))
        return groups


class AutocompleteSelectMultiple(AutocompleteMixin, forms.SelectMultiple):
    pass


class MultipleChoiceFilterWidget(forms.widgets.CheckboxSelectMultiple):
    """A basic multi checkbox widget with a custom template.

    We can't override the default template because it would mess with the
    django admin.
    """

    template_name = "forms/widgets/multiple_input.html"


class SelectWidgetWithDisabledEmptyOption(forms.Select):
    """
    Subclass of Django's select widget that allows a
    disabled hidden empty option
    """

    def create_option(self, *args, **kwargs):
        option_dict = super().create_option(*args, **kwargs)
        if option_dict["value"] == "":
            option_dict["attrs"]["disabled"] = "disabled"
            option_dict["attrs"]["hidden"] = "hidden"
        return option_dict
