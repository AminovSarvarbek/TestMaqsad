from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def admin_only(view_func):
    """
    Custom decorator to allow access only to admin users.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect(reverse('custom_admin:admin_login'))
        
        # Check if the user is an admin (superuser or staff)
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You do not have the necessary permissions.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
