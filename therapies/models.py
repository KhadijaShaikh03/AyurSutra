from django.db import models
from patients.models import Patient


class Therapy(models.Model):
    therapy_name = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.therapy_name


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    def __str__(self):
        return f"{self.patient} - {self.therapy} on {self.date}"