from django.urls import path
app_name = 'cinema'
from cinema.views import *

urlpatterns  = [
    path('', HomeView.as_view(), name='home'),
    # path('movie', MovieView.as_view(), name='movie'),
    # path('movie-detail/<slug>', MovieDetailView.as_view(), name='movie-detail'),
    # path('seat/<slug>/<int:date_id>/<int:show_id>', Seatview.as_view(), name='seat'),
    # path('reserve/<int:seat_id>/<int:date_id>/<int:show_id>/<slug>', ReserveView.as_view(), name = 'reserve'),
    # path('booking/<int:seat_id>/', BookingView.as_view(), name='booking'),
    # path('login', LoginView.as_view(), name='login'), 
    # path('signup',SignupView.as_view(), name='signup'),
    # path('logout', LogoutView.as_view(), name='logout'),
    # path('activate/<uidb64>/<token>',activate, name='activate'),
    # path('search', MovieSearchView.as_view(), name = 'search'),
    # path('showtime/<int:id>/<str:slug>', MovieShowTimeView.as_view(), name='showtime'),
    # path('funcsignup', signup, name='funcsignup')
]



