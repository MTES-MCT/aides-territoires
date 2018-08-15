from django import forms


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
