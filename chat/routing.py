from django.urls import path
from .consumers import ApiConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:user_id>/', ApiConsumer.as_asgi()),  # Websocket URL
]
