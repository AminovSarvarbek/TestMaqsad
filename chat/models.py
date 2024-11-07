from django.db import models
from user.models import CustomUser


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    admin = models.ForeignKey(CustomUser, related_name='admin_messages', null=True, blank=True, on_delete=models.SET_NULL)
    message = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen_by_admin = models.BooleanField(default=False)
    seen_by_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.message[:20]}"

    class Meta:
        ordering = ['timestamp']