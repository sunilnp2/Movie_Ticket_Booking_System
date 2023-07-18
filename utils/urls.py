app_name = 'utils'
from utils.views import testmail
from django.urls import path

urlpatterns = [
    path("testurl", testmail, name="testurl"),
    ]
