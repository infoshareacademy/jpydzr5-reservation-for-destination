from django import forms
from .models import *
import pendulum


class SeatForm(forms.Form):
    """Formularz wyboru miejsc"""
    seat = forms.ModelChoiceField(queryset=Seat.objects.none(), label="Wybierz miejsce")

    def __init__(self, *args, **kwargs):
        seance = kwargs.pop('seance', None)
        super().__init__(*args, **kwargs)
        if seance:
            # Filtrowanie miejsc na podstawie seansu
            self.fields['seat'].queryset = Seat.objects.filter(hall=seance.hall)


class MovieForm(forms.Form):
    """Formularz wyboru filmu"""
    movie = forms.ModelChoiceField(queryset=Movie.objects.filter(seances__show_start__gte=pendulum.now().subtract(minutes=30)).distinct(), label="Wybierz film")


class SeanceForm(forms.Form):
    """Formularz wyboru seansu"""
    show_start = forms.ModelChoiceField(queryset=Seance.objects.none(), label="Wybierz seans")

    def __init__(self, *args, **kwargs):
        movie = kwargs.pop('movie', None)
        super().__init__(*args, **kwargs)
        if movie:
            self.fields['show_start'].queryset = Seance.objects.filter(
                movie=movie,
                show_start__gte=pendulum.now().subtract(minutes=30)
            ).order_by('show_start')


class TicketTypeForm(forms.Form):
    """Formularz wyboru typu biletu"""
    ticket_type = forms.ModelChoiceField(
        queryset=TicketType.objects.all(),
        label='Typ biletu',
        empty_label="Wybierz typ biletu"
    )

