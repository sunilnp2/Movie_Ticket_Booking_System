from django.urls import path
from api.views import SingupSerializerView


app_name = 'api'

urlpatterns = [
    path('signup/', SingupSerializerView.as_view(), name='signup'),
]