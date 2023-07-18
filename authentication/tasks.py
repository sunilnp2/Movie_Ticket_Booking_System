from django.conf import settings
from celery import shared_task
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from authentication.views import *

from django.core.mail import send_mail

@shared_task(bind = True)
def activate_email(request,id,domain, uid, token, protocol):
    user = User.objects.get(id = id)
    name = user.username
    email = user.email
    domain = domain
    uid = uid
    token = token
    protocol = protocol
    activate_url = f"{protocol}://{domain}/auth/activate/{uid}/{token}"
    print(f"The url is {activate_url}")
    mail_subject = "Activate your user account."
    message = render_to_string("email-activate.html", {
        'user': user.first_name,
        'domain': domain,
        'uid': uid,
        'token': token,
        "protocol": protocol,
    })
    # email = EmailMessage(mail_subject, message, to=[email])
    # email.send()
    send_mail(
            subject= mail_subject,
            message= message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True,

        )
    return "Done"

