from django.urls import path
from . import views

urlpatterns = [
    # Therapies
    path('', views.therapy_list, name='therapies'),
    path('add/', views.add_therapy, name='add_therapy'),
    path('edit/<int:id>/', views.edit_therapy, name='edit_therapy'),
    path('delete/<int:id>/', views.delete_therapy, name='delete_therapy'),
    # Appointments (inside therapies)
    path('appointments/', views.appointment_list, name='appointments'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('<int:pk>/delete/', views.delete_appointment, name='appointment_delete'),
    
    # Calendar
    path('calendar/', views.appointment_calendar, name='appointment_calendar'),

    # Status update
    path('update-status/<int:pk>/', views.update_status, name='update_status'),
]