from django.shortcuts import render, get_object_or_404, redirect
from .models import Therapy, Appointment
from datetime import date
import calendar
from django.db.models import Q
from django import forms
from .forms import AppointmentForm
from django.http import JsonResponse


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
    return render(request, 'therapies/appointment_detail.html', {
        'appointment': appointment
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
def edit_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appt)

    if form.is_valid():
        form.save()
        return redirect('appointments')

    return render(request, 'therapies/appointment_form.html', {'form': form})

    return render(request, 'therapies/appointment_form.html', {'form': form})
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()   # ✅ no need to manually set status
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