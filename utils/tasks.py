from time import sleep
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from celery import shared_task
from django.conf import settings
from authentication.models import User



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
def send_ticket(self,id, pdf_tuple):
    user_email = User.objects.get(id = id).email
    subject = 'Your Movie Ticket Booking'
    message = 'Thank you for booking your movie ticket with us!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    # for sending email
     # Save the PDF to a temporary file

    pdf_file_name, pdf_content, content_type = pdf_tuple
        
        # Send the email with the PDF attachment
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(pdf_file_name, pdf_content, content_type)
    email.send()
      # Remove the temporary file after sending the email
    return "Done"