from django.shortcuts import render
from .models import TrafficData
import matplotlib.pyplot as plt
import io, base64

def dashboard(request):
    data = TrafficData.objects.all().order_by('-timestamp')[:10]

    # Adaptive logic: green light time proportional to vehicle count
    adaptive_times = {d.intersection: max(10, d.vehicle_count * 2) for d in data}

    # Visualization
    intersections = [d.intersection for d in data]
    counts = [d.vehicle_count for d in data]

    plt.figure(figsize=(6,4))
    plt.bar(intersections, counts, color='green')
    plt.title("Traffic Density")
    plt.xlabel("Intersection")
    plt.ylabel("Vehicle Count")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, "dashboard.html", {"chart": chart, "adaptive_times": adaptive_times})