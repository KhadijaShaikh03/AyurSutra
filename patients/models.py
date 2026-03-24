from django.db import models

class Patient(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return self.name