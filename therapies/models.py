from django.db import models
from patients.models import Patient


class Therapy(models.Model):
    therapy_name = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    description = models.TextField()
    precautions = models.TextField(blank=True)
    def __str__(self):
        return self.therapy_name


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="therapy_appointments")
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    doctor_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient} - {self.therapy} on {self.date}"
    
class Precaution(models.Model):
    PRE_POST_CHOICES = (
        ('before', 'Before Therapy'),
        ('after', 'After Therapy'),
    )

    appointment = models.ForeignKey(
        'Appointment',
        on_delete=models.CASCADE,
        related_name='precautions'
    )

    type = models.CharField(
        max_length=10,
        choices=PRE_POST_CHOICES
    )

    text = models.TextField()

    def __str__(self):
        return f"{self.appointment} - {self.type}"
    
class Prescription(models.Model):
    appointment = models.ForeignKey(
    'Appointment',
    on_delete=models.CASCADE,
    related_name='prescriptions'
    )
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medicine_name
    
class DietPlan(models.Model):
    PRE_POST_CHOICES = (
        ('before', 'Before Therapy'),
        ('after', 'After Therapy'),
    )

    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=PRE_POST_CHOICES)

    morning = models.TextField(blank=True, null=True)
    afternoon = models.TextField(blank=True, null=True)
    evening = models.TextField(blank=True, null=True)
    night = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Diet Plan for {self.appointment}"
    
class TherapyPrecaution(models.Model):
    PRE_POST_CHOICES = (
        ('before', 'Before Therapy'),
        ('after', 'After Therapy'),
    )

    therapy = models.ForeignKey('Therapy', on_delete=models.CASCADE, related_name='default_precautions')
    type = models.CharField(max_length=10, choices=PRE_POST_CHOICES)
    text = models.TextField()

    def __str__(self):
        return f"{self.therapy.therapy_name} - {self.type}"
    
class TherapyDietPlan(models.Model):
    PRE_POST_CHOICES = (
        ('before', 'Before Therapy'),
        ('after', 'After Therapy'),
    )

    therapy = models.ForeignKey('Therapy', on_delete=models.CASCADE, related_name='default_diets')
    type = models.CharField(max_length=10, choices=PRE_POST_CHOICES)

    morning = models.TextField(null=True, blank=True)
    afternoon = models.TextField(null=True, blank=True)
    evening = models.TextField(null=True, blank=True)
    night = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Diet - {self.therapy.therapy_name}"