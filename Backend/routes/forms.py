from django import forms
from .models import AirportRoute


class AirportRouteForm(forms.ModelForm):
    class Meta:
        model = AirportRoute
        fields = ['airport_code', 'position', 'duration', 'next_airport']

        widgets = {
            'airport_code': forms.TextInput(
                attrs={'placeholder': 'Enter airport code'}
            ),
            'position': forms.NumberInput(
                attrs={'placeholder': 'Enter position'}
            ),
            'duration': forms.NumberInput(
                attrs={'placeholder': 'Duration in minutes'}
            ),
            'next_airport': forms.TextInput(
                attrs={'placeholder': 'Next airport code'}
            ),
        }


class SearchRouteForm(forms.Form):
    airport_code = forms.CharField(max_length=10)
    n = forms.IntegerField(min_value=1)
    direction = forms.ChoiceField(
        choices=[
            ('left', 'Left'),
            ('right', 'Right'),
        ]
    )


class ShortestRouteForm(forms.Form):
    source = forms.CharField(max_length=10)
    destination = forms.CharField(max_length=10)