from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits"
)
class Patient(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=10, validators=[phone_validator])
    def save(self, *args, **kwargs):
        self.full_clean()   # 🔥 THIS IS CRITICAL
        super().save(*args, **kwargs)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Therapy(models.Model):
    therapy_name = models.CharField(max_length=100)
    duration = models.IntegerField()

    def __str__(self):
        return self.therapy_name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    therapy = models.ForeignKey(Therapy, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Pending','Pending'),('Completed','Completed'),('Cancelled','Cancelled')], default='Pending')

    def __str__(self):
        return f"{self.patient.name} - {self.therapy} on {self.date}"