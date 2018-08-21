from django import forms
from django.utils.translation import ugettext_lazy as _

from aids.models import Aid


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

    def clean(self):
        data = super().clean()

        application_perimeter = data.get('application_perimeter')
        department = data.get('application_department')
        region = data.get('application_region')

        # Let's make sure that all the required data is set
        if application_perimeter == Aid.PERIMETERS.department:
            if not department:
                msg = _('You must provided the application department.')
                self.add_error('application_department', msg)
        else:
            if department:
                msg = _('This value must be blank.')
                self.add_error('application_department', msg)

        if application_perimeter == Aid.PERIMETERS.region:
            if not region:
                msg = _('You must provided the application region.')
                self.add_error('application_region', msg)
        else:
            if region:
                msg = _('This value must be blank.')
                self.add_error('application_region', msg)

        return data


class AidSearchForm(forms.Form):
    """Main form for search engine."""

    zipcode = forms.CharField(
        label=_('Zip code'),
        required=False,
        max_length=8)

    def filter_queryset(self, qs):
        """Filter querysets depending of input data."""

        return qs
