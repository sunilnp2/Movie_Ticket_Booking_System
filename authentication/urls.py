app_name = 'authentication'
from authentication.views import *
from django.urls import path, include

urlpatterns = [
        path('login/', LoginView.as_view(), name='login'), 
    path('signup',SignupView.as_view(), name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', ProfileView.as_view(), name = 'profile'),
    path('activate/<uidb64>/<token>',activate, name='activate'),
    
    # for api
    path('api/', include('authentication.api.urls')),
]
