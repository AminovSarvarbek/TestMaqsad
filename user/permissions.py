from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta

class IsAuthenticatedAndRecent(permissions.BasePermission):
    """
    Foydalanuvchi autentifikatsiyadan o'tganligini va oxirgi faoliyatini tekshirish.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        now = timezone.now()
        if request.user.last_login and request.user.last_login < now - timedelta(days=30):
            request.user.is_active = False
            request.user.save()
            return False

        return True