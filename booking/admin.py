from django.contrib import admin
from booking.models import *
# Register your models here.


class SeatAdmin(admin.ModelAdmin):
    list_display = ['id','seat_number', 'name']
admin.site.register(Seat, SeatAdmin)

admin.site.register(SeatAvailability)
