from django.forms import ModelMultipleChoiceField

from categories.models import Category


class CategoryMultipleChoiceField(ModelMultipleChoiceField):
    """Custom field to select categories."""

    def __init__(self, **kwargs):
        default_qs = Category.objects \
            .select_related('theme') \
            .order_by('theme__name', 'name')
        queryset = kwargs.pop('queryset', default_qs)
        super().__init__(queryset, **kwargs)

    def label_from_instance(self, obj):
        return '{} > {}'.format(obj.theme.name.upper(), obj)
