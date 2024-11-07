from django.core.mail import send_mail
from django.conf import settings
from background_task import background

@background(schedule=60)  # 60 soniya kutish
def custom_send_email(subject, message, recipient_list, fail_silently=False):
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=fail_silently)

# Taskni chaqirish
# custom_send_email('Subject here', 'Here is the message.', ['to@example.com'])
