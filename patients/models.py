from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

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
    
# ==============================
# 🔔 REMINDER MODEL
# ==============================
class Reminder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reminders')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    reminder_date = models.DateField()
    reminder_time = models.TimeField()

    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.patient.name}"


# ==============================
# ⚠️ PRECAUTION MODEL
# ==============================
class Precaution(models.Model):
    therapy = models.ForeignKey(
    Therapy,
    on_delete=models.CASCADE,
    related_name='precautions',
    null=True,
    blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.therapy.therapy_name}"


# ==============================
# 🥗 DIET PLAN MODEL
# ==============================
class DietPlan(models.Model):
    therapy = models.ForeignKey(
    Therapy,
    on_delete=models.CASCADE,
    related_name='diet_plans',
    null=True,
    blank=True
    )
    morning = models.TextField(blank=True)
    afternoon = models.TextField(blank=True)
    evening = models.TextField(blank=True)
    night = models.TextField(blank=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Diet Plan for {self.therapy.therapy_name}"