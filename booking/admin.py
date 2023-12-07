from django.contrib import admin
from booking.models import *
# Register your models here.


class SeatAdmin(admin.ModelAdmin):
    list_display = ['id','seat_number', 'name', 'screen_visibility', 'seat_score']
admin.site.register(Seat, SeatAdmin)

class SeatAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'show_date', 'movie', 'seat', 'showtime', 'seat_status', 'morning', 'day', 'night', 'payment_status')
    list_display_links = ('user', 'show_date', 'movie', 'seat', 'showtime', 'seat_status', 'morning', 'day', 'night', 'payment_status')

admin.site.register(SeatAvailability, SeatAvailabilityAdmin)

class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'show_date','book_seat', 'showtime', 'movie', 'reservation_datetime', 'payment_status', 'payment_method')

admin.site.register(BookingHistory, BookingHistoryAdmin)


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'payment_amount', 'timestamp']
    list_display_links = ['user', 'movie', 'payment_amount', 'timestamp']
admin.site.register(Collection, CollectionAdmin)