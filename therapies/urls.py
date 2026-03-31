from django.urls import path
from . import views

urlpatterns = [
    # Therapies
    path('', views.therapy_list, name='therapies'),

    # Appointments (inside therapies)
    path('appointments/', views.appointment_list, name='appointments'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/edit/', views.edit_appointment, name='appointment_edit'),
    path('<int:pk>/delete/', views.delete_appointment, name='appointment_delete'),

    # Calendar
    path('calendar/', views.appointment_calendar, name='appointment_calendar'),

    # Status update
    path('update-status/<int:pk>/', views.update_status, name='update_status'),
]