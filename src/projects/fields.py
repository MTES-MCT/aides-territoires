from django import forms


class ProjectMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Custom field to select projects."""

    def label_from_instance(self, obj):
        return "{} : {}".format(obj.name.upper(), obj.description)
