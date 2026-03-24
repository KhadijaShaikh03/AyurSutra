from django.contrib import admin
from django.urls import path

from patients.views import (
    dashboard,
    patient_list,
    add_patient,
    edit_patient,
    delete_patient
)

from therapies.views import therapy_list, appointment_list, appointment_calendar, appointment_detail, add_appointment, update_status

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard
    path('', dashboard, name='dashboard'),

    # Patients CRUD
    path('patients/', patient_list, name='patients'),
    path('patients/add/', add_patient, name='add_patient'),
    path('patients/edit/<int:pk>/', edit_patient, name='edit_patient'),   # ✅ FIXED
    path('patients/delete/<int:pk>/', delete_patient, name='delete_patient'),  # ✅ FIXED

    # Other modules
    path('therapies/', therapy_list, name='therapies'),
    path('appointments/', appointment_list, name='appointments'),
    path('appointments/calendar/', appointment_calendar, name='appointment_calendar'),
    path('appointments/<int:pk>/', appointment_detail, name='appointment_detail'),
    path('appointments/add/', add_appointment, name='add_appointment'),
    path('appointments/update-status/<int:pk>/', update_status, name='update_status'),
]