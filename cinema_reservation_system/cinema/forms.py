from django import forms
from .models import Seance, Price

# Formularz wyboru seansu
class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['movie', 'hall_number', 'show_start']
        labels = {
            'movie': 'Wybierz film',
            'hall_number': 'Sala',
            'show_start': 'Data i godzina seansu',
        }

# Formularz wyboru typu biletu
class TicketTypeForm(forms.Form):
    ticket_type = forms.ModelChoiceField(
        queryset=Price.objects.all(),
        label='Typ biletu',
        empty_label="Wybierz typ biletu"
    )