import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import TrafficData

class TrafficConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        # Example: fetch latest traffic data dynamically
        latest = TrafficData.objects.order_by("-timestamp")[:10]
        intersections = [d.intersection for d in latest]
        counts = [d.vehicle_count for d in latest]

        await self.send(text_data=json.dumps({
            "labels": intersections,
            "counts": counts,
        }))
