from django import forms

from .models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'active_ingredient', 'amount', 'dose', 'expiration_date']
        widgets = {'expiration_date': forms.DateInput(attrs={'type': 'date'})}