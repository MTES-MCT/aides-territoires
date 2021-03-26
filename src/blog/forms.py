from django import forms
from django.utils.translation import gettext_lazy as _

from blog.models import PostCategory
from blog.fields import PostCategoryChoiceField


class PostSearchForm(forms.Form):
    """form for filter posts by categorie."""

    category = PostCategoryChoiceField(
        label=_('You are seeking posts about…'),
        queryset=PostCategory.objects.all(),
        to_field_name='slug',
        required=False)
