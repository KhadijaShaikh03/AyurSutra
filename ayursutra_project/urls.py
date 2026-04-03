from django.contrib import admin
from django.urls import path, include
from patients.views import dashboard
from patients import views 

urlpatterns = [
    path('admin/', lambda request: redirect('/dashboard/')), 
    path('secure-admin/', admin.site.urls),
    # Dashboard
    path('', views.home, name='home'),

    # Patients
    path('patients/', include('patients.urls')),
    
    # ✅ Therapies + Appointments (handled inside app)
    path('therapies/', include('therapies.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('patient/login/', views.patient_login, name='patient_login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
]