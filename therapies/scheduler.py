from datetime import timedelta
from .models import Appointment

def generate_schedule(patient, therapy, start_date, sessions):

    schedule = []

    for i in range(sessions):

        date = start_date + timedelta(days=i)

        appointment = Appointment.objects.create(
            patient=patient,
            therapy=therapy,
            date=date,
            time="09:00",
            status="Scheduled"
        )

        schedule.append(appointment)

    return schedule