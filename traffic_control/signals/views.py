from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import TrafficData,SignalTiming, IncidentReport
import matplotlib.pyplot as plt
import io, base64
from .forms import IncidentReportForm, TrafficFilterForm
import json



# Registration
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # after register go to login
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

# Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")  # after login go to dashboard
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# Logout
def logout_view(request):
    logout(request)
    return redirect("login")  # after logout go back to login



# Dashboard

@login_required(login_url="login")
def dashboard(request):
    # Handle incident form submission
    if request.method == "POST":
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.save()
            return redirect("dashboard")
    else:
        form = IncidentReportForm()

    # Apply filters
    filter_form = TrafficFilterForm(request.GET or None)
    qs = TrafficData.objects.all()
    if filter_form.is_valid():
        if filter_form.cleaned_data["start_date"]:
            qs = qs.filter(timestamp__gte=filter_form.cleaned_data["start_date"])
        if filter_form.cleaned_data["end_date"]:
            qs = qs.filter(timestamp__lte=filter_form.cleaned_data["end_date"])
        if filter_form.cleaned_data["intersection"]:
            qs = qs.filter(intersection__icontains=filter_form.cleaned_data["intersection"])

    # Traffic chart data
    data = qs.order_by('-timestamp')[:10]
    intersections = [d.intersection for d in data]
    counts = [d.vehicle_count for d in data]

    chart_data = {
        "labels": json.dumps(intersections),
        "counts": json.dumps(counts),
    }

    # Signal timings chart data
    timings = SignalTiming.objects.all()
    intersections_t = [t.intersection for t in timings]
    green_times = [t.green_time for t in timings]
    red_times = [t.red_time for t in timings]

    timing_data = {
        "labels": json.dumps(intersections_t),
        "green_times": json.dumps(green_times),
        "red_times": json.dumps(red_times),
    }

    # Incident reports
    incidents = IncidentReport.objects.order_by('-timestamp')[:5]

    return render(request, "dashboard.html", {
        "chart_data": chart_data,
        "timing_data": timing_data,
        "incidents": incidents,
        "form": form,
        "filter_form": filter_form,
    })