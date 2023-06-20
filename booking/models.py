from django.db import models
from movie.models import *
from authentication.models import User
SEAT_STATUS = (('available', 'available'), ('pending', 'pending'), ('reserved', 'reserved'))


# Create your models here.
class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    name = models.CharField(max_length=10)
    status = models.CharField(choices=SEAT_STATUS, max_length=100,blank=True, null=True)

    def __str__(self):
        return str(self.seat_number)


class SeatAvailability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.ForeignKey(MovieDate, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    status = models.CharField(choices=SEAT_STATUS, max_length=20, default='available')
    morning = models.BooleanField(default=True)
    day = models.BooleanField(default=True)
    night = models.BooleanField(default=True)
    payment_status = models.BooleanField(default=False)
    total = models.PositiveBigIntegerField(default=0,null=True, blank=True)


    def __str__(self):
        return f"Seat {self.seat.seat_number} Availability"
    class Meta:
        db_table = 'seatavailability'
        ordering = ('movie',)


class BookingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_date = models.ForeignKey(MovieDate, on_delete=models.CASCADE, null=True, blank=True)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    reservation_datetime = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    total = models.PositiveBigIntegerField(default=0,null=True, blank=True)

    def __str__(self):
        return self.movie.name


