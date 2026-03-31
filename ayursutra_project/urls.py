from django.contrib import admin
from django.urls import path, include
from patients.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard
    path('', dashboard, name='dashboard'),

    # Patients
    path('patients/', include('patients.urls')),
    
    # ✅ Therapies + Appointments (handled inside app)
    path('therapies/', include('therapies.urls')),
]