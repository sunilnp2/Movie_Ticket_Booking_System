from django.urls import path, include
app_name = 'cinema'
from cinema.views import *

urlpatterns  = [
    path('', HomeView.as_view(), name='home'),

        # for api
    path('api/', include('cinema.api.urls')),
]



