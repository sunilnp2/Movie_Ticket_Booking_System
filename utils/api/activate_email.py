from authentication.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from utils.api.jwt_tokens import generate_token
from authentication.api.tasks import drf_activate_email


def activateEmail(request,email):
    user = User.objects.get(email = email)
    username = User.objects.get(email=email).username
    id = user.id
    domain =  get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = generate_token(user)
    protocol = 'https' if request.is_secure() else 'http'
    drf_activate_email.delay(id, domain, uid, token, protocol)
    