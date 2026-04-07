from django.shortcuts import render, get_object_or_404, redirect
from .models import Therapy, Appointment,TherapyPrecaution, TherapyDietPlan,Precaution,DietPlan,Prescription
from datetime import date
import calendar
from django.db.models import Q
from django import forms
from .forms import AppointmentForm
from django.http import JsonResponse
from .forms import TherapyForm
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.db.models import ProtectedError
from django.contrib import messages

def therapy_list(request):
    therapies = Therapy.objects.all()
    return render(request, 'therapies/therapy_list.html', {'therapies': therapies})


def appointment_list(request):
    status_filter = request.GET.get('status')
    query = request.GET.get('q')

    appointments = Appointment.objects.all().order_by('-date', '-time')

    # FILTER BY STATUS
    if status_filter:
        appointments = appointments.filter(status=status_filter)

    # SEARCH
    if query:
     appointments = appointments.filter(
        Q(patient__name__icontains=query) |
        Q(therapy__therapy_name__icontains=query)
    )

    return render(request, 'therapies/appointment_list.html', {
        'appointments': appointments,
        'status_filter': status_filter,
        'query': query
    })


# 📅 CALENDAR VIEW
def appointment_calendar(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    cal = calendar.monthcalendar(year, month)

    appointments = Appointment.objects.filter(
        date__year=year,
        date__month=month
    )

    appointment_dict = {}
    for appt in appointments:
      day = appt.date.day   # ✅ INDENTED
      if day not in appointment_dict:
        appointment_dict[day] = []
      appointment_dict[day].append(appt)

    context = {
        'calendar': cal,
        'appointment_dict': appointment_dict,
        'month': month,
        'year': year,
    }
    return render(request, 'therapies/appointment_calendar.html', context)
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointments = Appointment.objects.filter(
        patient=appointment.patient
    ).exclude(id=appointment.id)

    past_prescriptions = Prescription.objects.filter(
        appointment__in=appointments
    )
    precautions = Precaution.objects.filter(appointment=appointment)
    diets = DietPlan.objects.filter(appointment=appointment)

    prescriptions = appointment.prescriptions.all()  # ✅ IMPORTANT

    if request.method == "POST":
        medicine = request.POST.get("medicine")
        dosage = request.POST.get("dosage")
        duration = request.POST.get("duration")

        if medicine and dosage and duration:
            Prescription.objects.create(
                appointment=appointment,
                medicine_name=medicine,  
                dosage=dosage,
                duration=duration
            )

        return redirect("appointment_detail", pk=appointment.id)

    return render(request, "therapies/appointment_detail.html", {
        "appointment": appointment,
        "precautions": precautions,
        "diets": diets,
        "prescriptions": prescriptions,
        "past_prescriptions": past_prescriptions,
    })
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appointment)

    if form.is_valid():
        form.save()
        return redirect('appointments')

    return render(request, 'therapies/appointment_form.html', {'form': form})


def delete_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.delete()
    return redirect('appointments')

def update_status(request, pk):
    appt = Appointment.objects.get(pk=pk)
    if request.method == "POST":
        new_status = request.POST.get('status')
        appt.status = new_status
        appt.save()
        return redirect('appointments')   # ✅ FIX

    return redirect('appointments')

@login_required
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()   # ✅ FIXED

            # 🔹 Copy precautions
            defaults = TherapyPrecaution.objects.filter(
                therapy=appointment.therapy
            )
            for p in defaults:
                Precaution.objects.create(
                    appointment=appointment,
                    type=p.type,
                    text=p.text
                )

            # 🔹 Copy diet plans
            diets = TherapyDietPlan.objects.filter(
                therapy=appointment.therapy
            )
            for d in diets:
                DietPlan.objects.create(
                    appointment=appointment,
                    type=d.type,
                    morning=d.morning,
                    afternoon=d.afternoon,
                    evening=d.evening,
                    night=d.night
                )

            return redirect('appointments')
    else:
        form = AppointmentForm()

    return render(request, 'therapies/appointment_form.html', {
        'form': form
    })

def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return redirect('appointments')


def therapy_list(request):
    therapies = Therapy.objects.prefetch_related(
        'default_precautions',
        'default_diets'
    )
    return render(request, 'therapies/therapy_list.html', {
        'therapies': therapies
    })
@login_required
def add_therapy(request):
    if request.method == 'POST':
        form = TherapyForm(request.POST)
        if form.is_valid():
            therapy = form.save()

            # 🔹 Precautions
            before_precautions = request.POST.getlist('before_precaution')
            after_precautions = request.POST.getlist('after_precaution')

            for p in before_precautions:
                if p.strip():
                    TherapyPrecaution.objects.create(
                        therapy=therapy,
                        type='before',
                        text=p
                    )

            for p in after_precautions:
                if p.strip():
                    TherapyPrecaution.objects.create(
                        therapy=therapy,
                        type='after',
                        text=p
                    )

            # 🔹 Diet Plan (Before)
            TherapyDietPlan.objects.create(
                therapy=therapy,
                type='before',
                morning=request.POST.get('before_morning'),
                afternoon=request.POST.get('before_afternoon'),
                evening=request.POST.get('before_evening'),
                night=request.POST.get('before_night'),
            )

            # 🔹 Diet Plan (After)
            TherapyDietPlan.objects.create(
                therapy=therapy,
                type='after',
                morning=request.POST.get('after_morning'),
                afternoon=request.POST.get('after_afternoon'),
                evening=request.POST.get('after_evening'),
                night=request.POST.get('after_night'),
            )

            return redirect('therapies')

    else:
        form = TherapyForm()

    return render(request, 'therapies/add_therapy.html', {'form': form})

@login_required
def edit_therapy(request, id):
    therapy = get_object_or_404(Therapy, id=id)

    if request.method == 'POST':
        form = TherapyForm(request.POST, instance=therapy)
        if form.is_valid():
            form.save()
            messages.success(request, "Therapy updated successfully.")
            return redirect('therapies')
        else:
            messages.error(request, "Error updating therapy.")
    else:
        form = TherapyForm(instance=therapy)

    return render(request, 'therapies/add_therapy.html', {
        'form': form,
        'is_edit': True
    })

@login_required
def delete_therapy(request, id):
    therapy = Therapy.objects.get(id=id)

    if request.method == 'POST':
        try:
            therapy.delete()
        except ProtectedError:
            messages.error(request, "Cannot delete therapy linked to appointments.")
            return redirect('therapies')

        return redirect('therapies')

    return render(request, 'therapies/delete_therapy.html', {
        'therapy': therapy
    })