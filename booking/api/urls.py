from django.urls import path
from booking.api.views import SeatAPIView, SeatReserveAPIView, BookPenHisAPIView, BookingAPIView, PaymentAPIView

urlpatterns = [
    path('api_seat', SeatAPIView.as_view(), name='api_seat'),
    path('seat_reserve/<int:seat_id>/<str:movie_slug>/<int:show_id>/<int:hall_id>/', SeatReserveAPIView.as_view(), name='seat-reserve'),
    
    # for showing booking pending and booking histroy of user to admin 
    path('book_pen_his',BookPenHisAPIView.as_view(), name='book_pen_his'),
    
    # for booking confirmation and pay
    path('drf_booking/<str:slug>/<int:show_id>/<int:hall_id>/', BookingAPIView.as_view(), name='drf_booking'),
    
    # code for payment
    path('api_payment/<str:slug>/<int:show_id>/<int:hall_id>', PaymentAPIView.as_view(), name='api_payment'),
]
