from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages


def patient_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("patient_dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "patients/login.html")


def patient_logout(request):
    logout(request)
    return redirect("patient_login")