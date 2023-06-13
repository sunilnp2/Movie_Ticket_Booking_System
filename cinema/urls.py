from django.urls import path
app_name = 'cinema'
from cinema.views import *

urlpatterns  = [
    path('', HomeView.as_view(), name='home'),
    path('movie', MovieView.as_view(), name='movie'),
    path('movie-detail/<slug>', MovieDetailView.as_view(), name='movie-detail'),
    path('seat', Seatview.as_view(), name='seat'),
    path('booking', BookingView.as_view(), name='booking'),
    path('login', LoginView.as_view(), name='login'), 
    path('signup',SignupView.as_view(), name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>',activate, name='activate'),
    path('search', MovieSearchView.as_view(), name = 'search'),
    path('showtime/<int:id>/<str:slug>', MovieShowTimeView.as_view(), name='showtime'),
    # path('funcsignup', signup, name='funcsignup')
]



