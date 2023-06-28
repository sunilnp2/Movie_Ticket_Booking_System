from django.urls import path 
app_name = 'booking'
from booking.views import *



urlpatterns = [
    path('seat/<slug>/<int:date_id>/<int:show_id>/<int:hall_id>', Seatview.as_view(), name='seat'),
    path('reserve/<int:seat_id>/<int:date_id>/<int:show_id>/<slug>/<int:hall_id>', ReserveView.as_view(), name = 'reserve'),
    path('booking/<slug>/<int:date_id>/<int:show_id>/<int:hall_id>', BookingView.as_view(), name='booking'),
    path('payment/<slug>/<int:date_id>/<int:show_id>/<int:hall_id>', PaymentView.as_view(), name='payment'),
    path('history', BookingHostoryView.as_view(), name = "history"),
    path('bookingadmin', AdminBookingView.as_view(), name='bookingadmin'),
    path('deletepending/<int:id>', DeletePendingView.as_view(), name='deletepending'),
    path('hisdelete/<int:id>', BookingHistoryDeleteView.as_view(), name='hisdelete'),

    # url for jquery ajax 
    path('pending/delete/', DeleteBookingView.as_view(), name='delete_pending'),
]
