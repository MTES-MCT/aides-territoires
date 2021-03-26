from django import forms


class PostCategoryChoiceField(forms.ModelChoiceField):
    """Custom field to select projects."""

    def label_from_instance(self, obj):
        return '{}'.format(obj.name)
