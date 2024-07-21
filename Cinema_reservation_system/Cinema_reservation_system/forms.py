from django import forms
from django.core.exceptions import ValidationError


class ChooseOptionMenuForm(forms.Form):
    input_value_menu = forms.CharField(max_length=1, label="", widget=forms.TextInput(attrs={"size": 1}))

    def clean_input_value_menu(self):
        value = self.cleaned_data.get("input_value_menu")
        if value not in ["1", "2", "3", "4"]:
            raise ValidationError("Proszę wybrać 1, 2, 3 lub 4!")
        return value
