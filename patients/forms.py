from django import forms
from .models import Patient
from therapies.models import Therapy

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'phone']

def clean_phone(self):
    phone = self.cleaned_data.get('phone')

    if not phone.isdigit() or len(phone) != 10:
        raise forms.ValidationError("Phone number must be exactly 10 digits")

    return phone