
from django.urls import path
from .views import SignUpSerializerView, LoginSerializerView
from utils.api.jwt_tokens import VerifyTOkenView, RefreshToken


urlpatterns = [
    path('api_signup/', SignUpSerializerView.as_view(), name='api_signup'),
    path('api_login/', LoginSerializerView.as_view(), name = 'api_login'),
    path('drf_activate/<uidb64>/<token>/',VerifyTOkenView.as_view(), name='drf_activate'),
]

