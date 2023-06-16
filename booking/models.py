from django.db import models
from movie.models import *
SEAT_STATUS = (('available', 'available'), ('pending', 'pending'), ('reserved', 'reserved'))


# Create your models here.
class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    name = models.CharField(max_length=10)
    status = models.CharField(choices=SEAT_STATUS, max_length=100,blank=True, null=True)

    def __str__(self):
        return str(self.seat_number)


class SeatAvailability(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    status = models.CharField(choices=SEAT_STATUS, max_length=20, null=True, blank=True)
    morning = models.BooleanField(default=True)
    day = models.BooleanField(default=True)
    night = models.BooleanField(default=True)

    def __str__(self):
        return f"Seat {self.seat.seat_number} Availability"