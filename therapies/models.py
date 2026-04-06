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
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    prescription = models.TextField(blank=True, null=True)
    doctor_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient} - {self.therapy} on {self.date}"
    
class Precaution(models.Model):
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE, related_name='therapy_precautions')

    title = models.CharField(max_length=200)

    before_therapy = models.TextField(blank=True, null=True)
    after_therapy = models.TextField(blank=True, null=True)

    general_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.therapy.therapy_name} - {self.title}"
    
class Prescription(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)  # ✅ ADD THIS

    def __str__(self):
        return self.medicine_name