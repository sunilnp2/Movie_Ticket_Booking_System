from time import sleep
from django.core.mail import send_mail
from django.http import HttpResponse
from celery import shared_task
from django.conf import settings

@shared_task(bind = True)
def my_mail(self):
        """Sends an email when the feedback form has been submitted."""
        # Simulate expensive operation(s) that freeze Django
        subject = "Hello"
        message = "This is message after test"
        to_email = "suniltest@yopmail.com"
        send_mail(
            subject= subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,

        )
        return "Done"
    
    
@shared_task(bind = True)
def send_ticket(*args):
    to_email = "suniltest@yopmail.com"
    send_mail(
            subject= "ello",
            message= args,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,

        )
    return "Done"