from django.shortcuts import render, get_object_or_404, redirect
from .models import Therapy, Appointment
from datetime import date
import calendar
from django.db.models import Q
from django import forms
from .forms import AppointmentForm


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
def add_appointment(request):
    form = AppointmentForm(request.POST or None)

    if request.method == 'POST':
      form = AppointmentForm(request.POST)
    if form.is_valid():
        appointment = form.save(commit=False)
        appointment.status = form.cleaned_data['status']   # ✅ force save
        appointment.save()
        return redirect('appointments')
    else:
      form = AppointmentForm()

    return render(request, 'therapies/appointment_form.html', {
        'form': form
    })
def update_status(request, pk):
    appt = Appointment.objects.get(pk=pk)

    if request.method == "POST":
        new_status = request.POST.get('status')
        appt.status = new_status
        appt.save()

    return redirect('appointments')