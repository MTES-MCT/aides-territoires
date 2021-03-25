from django import forms
from django.utils.translation import gettext_lazy as _

from blog.models import Post


class PostSearchForm(forms.ModelForm):
    """form for filter posts by categorie."""

    POST_CATEGORIES = (
        ('', _('')),
        ('webinar', _('webinar')),
        ('newsletter', _('newsletter')),
        ('communication', _('communication')),
        ('team', _('team')),
    )

    categorie = forms.MultipleChoiceField(
        label=_('You are seeking posts about…'),
        required=False,
        choices=POST_CATEGORIES,
        widget=forms.Select)

    class Meta:
        model = Post
        fields = ["categorie"]
