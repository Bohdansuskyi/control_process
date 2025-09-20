
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


class TemperatureThresholdForm(forms.Form):
    max_temp = forms.FloatField(
        label="Górny próg temperatury dopuszczalnej",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'np. 18'
        })
    )
    min_temp = forms.FloatField(
        label="Dolny próg temperatury dopuszczalnej",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'np. 15'
        })
    )