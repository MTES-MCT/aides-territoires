from django import forms
from django.utils.translation import ugettext_lazy as _


class AidAdminForm(forms.ModelForm):
    """Custom form form Aids in admin."""

    class Meta:
        widgets = {
            'mobilization_steps': forms.CheckboxSelectMultiple,
            'targeted_audiances': forms.CheckboxSelectMultiple,
            'aid_types': forms.CheckboxSelectMultiple,
            'destinations': forms.CheckboxSelectMultiple,
            'thematics': forms.CheckboxSelectMultiple,
        }


class AidSearchForm(forms.Form):
    """Main form for search engine."""

    zipcode = forms.CharField(
        label=_('Zip code'),
        required=False,
        max_length=8)

    def filter_queryset(self, qs):
        """Filter querysets depending of input data."""

        return qs
