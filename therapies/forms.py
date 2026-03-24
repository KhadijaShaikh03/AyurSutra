from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
            'status': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'patient': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'therapy': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }