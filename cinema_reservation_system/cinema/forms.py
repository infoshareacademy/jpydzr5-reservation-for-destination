from django import forms
from django.forms import formset_factory

from . import models
import pendulum
from django.contrib.auth.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class SeatForm(forms.Form):
    """Formularz wyboru miejsc"""
    seat = forms.ModelChoiceField(queryset=models.Seat.objects.none(), label="Wybierz miejsce")

    def __init__(self, *args, **kwargs):
        seance = kwargs.pop('seance', None)
        super().__init__(*args, **kwargs)
        if seance:
            # Filtrowanie miejsc na podstawie seansu
            self.fields['seat'].queryset = models.Seat.objects.filter(hall=seance.hall)


class MovieForm(forms.Form):
    """Formularz wyboru filmu"""
    movie = forms.ModelChoiceField(queryset=models.Movie.objects.filter(seances__show_start__gte=pendulum.now().subtract(minutes=30)).distinct(), label="Wybierz film")


class SeanceForm(forms.Form):
    """Formularz wyboru seansu"""
    show_start = forms.ModelChoiceField(queryset=models.Seance.objects.none(), label="Wybierz seans")

    def __init__(self, *args, **kwargs):
        movie = kwargs.pop('movie', None)
        super().__init__(*args, **kwargs)
        if movie:
            self.fields['show_start'].queryset = models.Seance.objects.filter(
                movie=movie,
                show_start__gte=pendulum.now().subtract(minutes=30)
            ).order_by('show_start')


class SeatTicketTypeForm(forms.ModelForm):
    ticket_type = forms.ModelChoiceField(
        queryset=models.TicketType.objects.none(),
        required=True,
        label="Wybierz typ biletu",
        empty_label = None,
    )
    seat = forms.ModelChoiceField(
        queryset=models.Seat.objects.all(),
        widget=forms.HiddenInput()
    )

    class Meta:
        model = models.Seat
        fields = ['ticket_type', 'seat']

    def __init__(self, *args, **kwargs):
        seat = kwargs.pop('seat', None)
        super().__init__(*args, **kwargs)
        if seat:
            self.fields['seat'].initial = seat
            self.seat = seat
            if seat.seat_type:
                self.fields['ticket_type'].queryset = seat.seat_type.allowed_ticket_types.all()
                first_ticket_type = self.fields['ticket_type'].queryset.first()
                if first_ticket_type:
                    self.fields['ticket_type'].initial = first_ticket_type


def generate_seat_ticket_forms(selected_seats):
    return [
        SeatTicketTypeForm(seat=seat, prefix=f'seat_{seat.id}')
        for seat in selected_seats
    ]


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        labels = {
            'username': 'Nazwa użytkownika',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Adres e-mail',
            'is_active': 'Aktywny',
        }
