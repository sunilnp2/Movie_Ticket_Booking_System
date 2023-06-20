from django.urls import path
app_name = 'cinema'
from cinema.views import *

urlpatterns  = [
    path('', HomeView.as_view(), name='home'),

]



