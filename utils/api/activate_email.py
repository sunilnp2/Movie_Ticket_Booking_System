from django.test import RequestFactory
from authentication.api.views import CustomTokenObtainPairView
from authentication.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from utils.api.jwt_tokens import generate_token
from authentication.api.tasks import drf_activate_email


def activateEmail(request,email):
    user = User.objects.get(email = email)
    custom_token_view = CustomTokenObtainPairView.as_view()

    # Simulate a POST request with user credentials
    request = RequestFactory().post('/auth/token/', data={'email': 'admin@gmail.com', 'password': 'admin123'})
    token_response = custom_token_view(request)

    # Get the token from the response
    access = token_response.data.get('access', None)
    refresh = token_response.data.get('refresh', None)

    id = user.id
    domain =  get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
<<<<<<< Updated upstream
    token = generate_token(user)
    access = token['access']
    refresh = token['refresh']
    protocol = 'https' if request.is_secure() else 'http'
    drf_activate_email.delay(id, domain, uid, protocol, access = access, refresh = refresh)
=======
    # token = generate_token(user)
    protocol = 'https' if request.is_secure() else 'http'
    drf_activate_email.delay(id, domain, uid, access, refresh, protocol)
    # drf_activate_email.delay(id, domain, uid, token, protocol)
>>>>>>> Stashed changes
    