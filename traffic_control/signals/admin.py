from django.contrib import admin
from .models import TrafficData, SignalTiming, IncidentReport

admin.site.register(TrafficData)
admin.site.register(SignalTiming)
admin.site.register(IncidentReport)
