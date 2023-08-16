
from django.conf import settings
from celery import shared_task
from django.template.loader import render_to_string
from authentication.views import *

from django.core.mail import send_mail

@shared_task(bind = True)
def drf_activate_email(request,id,domain, uid, protocol,access = None, refresh = None ):
    user = User.objects.get(id = id)
    name = user.username
    email = user.email
    domain = domain
    uid = uid
    access_token = access
    refresh_token = refresh
    protocol = protocol
    mail_subject = "Activate your user account."
    message = render_to_string("drf-email-activate.html", {
        'user': user.first_name,
        'username':name,
        'domain': domain,
        'uid': uid,
        'token': access_token,
        'refresh_token':refresh_token,
        "protocol": protocol,
    })
    send_mail(
            subject= mail_subject,
            message= message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True,

        )
    return "Done"


