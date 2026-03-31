from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    path('', views.patient_list, name='patients'),
    path('add/', views.add_patient, name='add_patient'),
    path('edit/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('delete/<int:pk>/', views.delete_patient, name='delete_patient'),

    # 🔐 Auth
    path("login/", auth_views.patient_login, name="patient_login"),
    path("logout/", auth_views.patient_logout, name="patient_logout"),

    # 👤 Patient Dashboard
    path("dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path('diet-plan/', views.patient_diet_plan, name='patient_diet_plan'),  # <- must exist
    path('prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
    path('precautions/', views.patient_precautions, name='patient_precautions'),
    #path('appointments/', views.appointments_list, name='appointments'),
    path('appointments/', views.patient_appointments, name='patient_appointments'),
]