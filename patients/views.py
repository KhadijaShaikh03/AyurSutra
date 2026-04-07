from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Patient
from .forms import PatientForm
from therapies.models import Therapy, Appointment, Precaution
from datetime import date
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from therapies.models import Appointment
from therapies.models import Prescription, Precaution
from django.contrib.auth import authenticate, login



def patient_list(request):
    if hasattr(request.user, 'patient') and not request.user.is_staff:
        return redirect('patient_dashboard')
    query = request.GET.get('q')

    patients = Patient.objects.all()
    for patient in patients:
        therapies = Appointment.objects.filter(patient=patient)\
            .values_list('therapy__therapy_name', flat=True)

        patient.therapy_list = ", ".join(set(therapies)) if therapies else "No Therapy"

    if query:
        patients = patients.filter(name__icontains=query)

    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'query': query
    })


def add_patient(request):
    if hasattr(request.user, 'patient') and not request.user.is_staff:
        return redirect('patient_dashboard')
    form = PatientForm(request.POST or None)

    if form.is_valid():
        patient = form.save(commit=False)
        phone = patient.phone
        email = patient.email

        username = phone
        password = phone  # basic for now

        # Prevent duplicate users
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists with this phone number.")
            return redirect('patients')

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # Link user to patient
        patient.user = user
        patient.save()

        messages.success(request, f"Patient created. Login username: {username}")

        return redirect('patients')

    return render(request, 'patients/patient_form.html', {'form': form})


# EDIT
def edit_patient(request, pk):
    if hasattr(request.user, 'patient') and not request.user.is_staff:
        return redirect('patient_dashboard')
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        return redirect('patients')  # ✅ FIXED
    return render(request, 'patients/patient_form.html', {'form': form})


# DELETE

def delete_patient(request, pk):
    if hasattr(request.user, 'patient') and not request.user.is_staff:
        return redirect('patient_dashboard')
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patients')  # ✅ FIXED
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})


@login_required
def dashboard(request):
    # 🔥 FORCE admin redirect away from /admin/
    if request.path.startswith('/admin'):
        return redirect('/dashboard/')
    # 🔹 ADMIN / DOCTOR
    if request.user.is_staff or request.user.is_superuser:


        total_patients = Patient.objects.count()
        total_therapies = Therapy.objects.count()
        total_appointments = Appointment.objects.count()

        gender_data = Patient.objects.values('gender').annotate(count=Count('gender'))
        gender_labels = [g['gender'] for g in gender_data]
        gender_counts = [g['count'] for g in gender_data]

        status_data = Appointment.objects.values('status').annotate(count=Count('status'))
        status_labels = [s['status'] for s in status_data]
        status_counts = [s['count'] for s in status_data]

        today = date.today()

        context = {
            'total_patients': total_patients,
            'total_therapies': total_therapies,
            'total_appointments': total_appointments,

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

    # 🔹 PATIENT USER
    elif hasattr(request.user, 'patient'):
        return redirect('patient_dashboard')

    # 🔹 FALLBACK (IMPORTANT — prevents loop)
    else:
        return redirect('patient_login')

def home(request):
    return render(request, 'patients/home.html')

@login_required
def patient_dashboard(request):

    # 🔴 IMPORTANT FIX (NO LOOP NOW)
    if not hasattr(request.user, 'patient'):
        return redirect('patient_login')

    patient = request.user.patient

    appointments = patient.therapy_appointments.all()\
    .select_related('therapy')\
    .order_by('-date', '-time')
    pending_count = appointments.filter(status="Pending").count()
    completed_count = appointments.filter(status="Completed").count()
    # Get unique therapies from appointments
    therapies = set(
        appointment.therapy for appointment in appointments if appointment.therapy
    )

    # Fetch precautions related to these therapies
    precautions = Precaution.objects.filter(
    appointment__therapy__in=therapies
    )

    # Collect prescriptions if they exist
    prescriptions = []
    for a in appointments:
        prescriptions.extend(a.prescriptions.all())

    return render(request, "patients/patient_dashboard.html", {
    "patient": patient,
    "appointments": appointments,
    "precautions": precautions,
    "prescriptions": prescriptions,
    "diet_plans": [],
    "pending_count": pending_count,
    "completed_count": completed_count,
    "reminders": [],
})

@login_required
def patient_diet_plan(request):
    patient = request.user.patient
    return render(request, "patients/patient_diet_plan.html", {"patient": patient})

@login_required
def patient_prescriptions(request):
    patient = request.user.patient

    prescriptions = Prescription.objects.filter(
    appointment__patient=patient
    ).order_by('-created_at')

    return render(request, 'patients/patient_prescriptions.html', {
        'prescriptions': prescriptions
    })

@login_required
def patient_precautions(request):
    patient = request.user.patient
    appointments = patient.therapy_appointments.all()
    therapies = [appt.therapy for appt in appointments]
    precautions = Precaution.objects.filter(therapy__in=therapies).distinct()
    return render(request, "patients/patient_precautions.html", {"precautions": precautions})




@login_required
def patient_appointments(request):
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient).select_related('therapy')

    return render(request, 'patients/patient_appointments.html', {
        'appointments': appointments
    })


def patient_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if hasattr(user, 'patient'):
                return redirect('patient_dashboard')
            else:
                return redirect('dashboard')

        else:
            return render(request, 'patients/login.html', {'error': 'Invalid credentials'})

    return render(request, 'patients/login.html')