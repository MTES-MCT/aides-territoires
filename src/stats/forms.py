from django import forms


class StatSearchForm(forms.Form):

    start_date = forms.DateTimeField(
        label="Date de début",
        required=True,
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': 'jj/mm/aaaa'}))

    end_date = forms.DateTimeField(
        label="Date de fin",
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': 'jj/mm/aaaa'}))
