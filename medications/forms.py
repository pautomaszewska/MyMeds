from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date

from .models import Medicine


def validate_date(value):
    if value < date.today():
        raise ValidationError('You cannot add expired meds to the database')


class MedicineForm(forms.ModelForm):
    expiration_date = forms.DateField(validators=[validate_date], widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Medicine
        fields = ['name', 'active_ingredient', 'amount', 'dose', 'expiration_date']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
