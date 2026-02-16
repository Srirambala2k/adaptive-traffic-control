from django.db import models
from django.contrib.auth.models import User


class TrafficData(models.Model):
    intersection = models.CharField(max_length=100)
    vehicle_count = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Signal Timing

class SignalTiming(models.Model):
    intersection = models.CharField(max_length=100)
    green_time = models.IntegerField()
    red_time = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.intersection} - Green: {self.green_time}s"

# New model: Incident Reports
class IncidentReport(models.Model):
    intersection = models.CharField(max_length=100)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incident at {self.intersection} - {self.timestamp}"

