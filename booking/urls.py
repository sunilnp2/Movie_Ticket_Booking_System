from django.urls import path 
app_name = 'booking'
from booking.views import *



urlpatterns = [
     path('seat/<slug>/<int:date_id>/<int:show_id>', Seatview.as_view(), name='seat'),
    path('reserve/<int:seat_id>/<int:date_id>/<int:show_id>/<slug>', ReserveView.as_view(), name = 'reserve'),
    path('booking', BookingView.as_view(), name='booking'),
]
