import random
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from .tasks import custom_send_email

User = get_user_model()

@receiver(post_save, sender=User)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        # Generate a 5-digit confirmation code
        confirmation_code = random.randint(10000, 99999)

        # Save the confirmation code to the user model
        instance.confirmation = confirmation_code
        instance.save()

        # Prepare and send the confirmation email
        subject = 'TestMaqsad confirmation'
        message = f'Your confirmation code is: {confirmation_code}'
        recipient_list = [instance.email]

        custom_send_email(subject, message, recipient_list)