from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Patient
from .forms import PatientForm
from therapies.models import Therapy, Appointment
from datetime import date


# LIST
def patient_list(request):
    query = request.GET.get('q')

    patients = Patient.objects.all()

    if query:
        patients = patients.filter(name__icontains=query)

    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'query': query
    })

# ADD
def add_patient(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('patients')  # ✅ FIXED
    return render(request, 'patients/patient_form.html', {'form': form})


# EDIT
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        return redirect('patients')  # ✅ FIXED
    return render(request, 'patients/patient_form.html', {'form': form})


# DELETE
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patients')  # ✅ FIXED
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})


# DASHBOARD
def dashboard(request):

    # Stats
    total_patients = Patient.objects.count()
    total_therapies = Therapy.objects.count()
    total_appointments = Appointment.objects.count()

    # Gender chart
    gender_data = Patient.objects.values('gender').annotate(count=Count('gender'))
    gender_labels = [g['gender'] for g in gender_data]
    gender_counts = [g['count'] for g in gender_data]

    # Status chart
    status_data = Appointment.objects.values('status').annotate(count=Count('status'))
    status_labels = [s['status'] for s in status_data]
    status_counts = [s['count'] for s in status_data]

    # NEW: Today's appointments
    today = date.today()

    context = {
        'total_patients': Patient.objects.count(),
        'total_therapies': Therapy.objects.count(),
        'total_appointments': Appointment.objects.count(),

        'today_appointments': Appointment.objects.filter(date=today),
        'upcoming_appointments': Appointment.objects.filter(date__gte=today)[:5],

        'gender_labels': gender_labels,
        'gender_counts': gender_counts,

        'status_labels': status_labels,
        'status_counts': status_counts,

        'pending_count': Appointment.objects.filter(status='PENDING').count(),
        'completed_count': Appointment.objects.filter(status='COMPLETED').count(),
        'cancelled_count': Appointment.objects.filter(status='CANCELLED').count(),
    }

    return render(request, 'patients/dashboard.html', context)