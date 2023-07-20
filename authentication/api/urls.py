from django.urls import path
from .views import SignUpSerializerView, VerifyTOkenView, LoginSerializerView


urlpatterns = [
    path('signup/', SignUpSerializerView.as_view(), name='signup'),
    path('login/', LoginSerializerView.as_view(), name = 'login'),
    path('drf_activate/<uidb64>/<token>/',VerifyTOkenView.as_view(), name='drf_activate'),
]
