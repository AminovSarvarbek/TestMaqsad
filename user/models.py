from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    confirmation = models.BigIntegerField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def save(self, *args, **kwargs):
        # Parolni hashlash
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)

        # Agar foydalanuvchi faol bo'lsa, oxirgi faoliyat vaqtini yangilash
        if self.is_active:
            self.last_activity = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email if self.email else "No email"