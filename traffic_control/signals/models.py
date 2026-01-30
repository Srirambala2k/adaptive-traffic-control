from django.db import models

class TrafficData(models.Model):
    intersection = models.CharField(max_length=100)
    vehicle_count = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)



