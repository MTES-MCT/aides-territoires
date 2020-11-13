from django import forms

from categories.models import Category


class CategoryChoiceIterator(forms.models.ModelChoiceIterator):
    """Custom iterator for the `Category` queryset.

    This class generates the list of choices to be rendered by the widget.

    Here we create a custom iterator to group the categories under their
    respective themes.

    Taken from https://stackoverflow.com/a/60076749
    """
    def theme_label(self, theme_name):
        return '----- {}'.format(theme_name)

    def category_label(self, category):
        return '{} > {}'.format(category.theme.name, category.name)

    def __iter__(self):
        group = ""
        subgroup = []
        for category in self.queryset:
            if not group:
                group = category.theme.name

            if group != category.theme.name:
                yield (self.theme_label(group), subgroup)
                group = category.theme.name
                subgroup = [(category.slug, self.category_label(category))]
            else:
                subgroup.append((category.slug, self.category_label(category)))
        yield (self.theme_label(group), subgroup)


class CategoryMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Custom field to select categories."""
    iterator = CategoryChoiceIterator

    def __init__(self, **kwargs):
        default_qs = Category.objects \
            .select_related('theme') \
            .order_by('theme__name', 'name')
        queryset = kwargs.pop('queryset', default_qs)
        super().__init__(queryset, **kwargs)

    def label_from_instance(self, obj):
        return '{} > {}'.format(obj.theme.name.upper(), obj)
