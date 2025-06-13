
from django import forms

# form for searching UID from database
class UIDSearchForm(forms.Form):
    uid = forms.CharField(
        max_length=20,
        label="Wpisz UID odlewu",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz, aby wyszukać...'
        })
    )
