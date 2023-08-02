from django.urls import path
from cinema.api.views import HomeAPiView

urlpatterns = [
    path('apihome',HomeAPiView.as_view(), name='apihome'),
]

