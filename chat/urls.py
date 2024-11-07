from django.urls import path
from .views import get_user_messages, get_user_info

urlpatterns = [
    path('info', get_user_info),
    path('messages', get_user_messages, name='get_messages'),
]