# serializer for Seat View
from rest_framework import serializers
from booking.models import SEAT_STATUS, SeatAvailability, Seat, BookingHistory, Collection
from authentication.models import User
from movie.models import Movie, Showtime
from cinema.models import CinemaHall
from rest_framework.response import Response
from django.utils import timezone

class SeatSerializer(serializers.Serializer):
    seat_number = serializers.IntegerField()
    name = serializers.CharField(max_length = 10)
    seat_status = serializers.ChoiceField(SEAT_STATUS,default = 'available')
    
class SeatAvailabilitySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    hall = serializers.PrimaryKeyRelatedField(queryset = CinemaHall.objects.all())
    show_date = serializers.DateField()
    movie = serializers.PrimaryKeyRelatedField(queryset =Movie.objects.all())
    seat = serializers.PrimaryKeyRelatedField(queryset = Seat.objects.all())
    showtime = serializers.PrimaryKeyRelatedField(queryset = Showtime.objects.all())
    seat_status = serializers.ChoiceField(SEAT_STATUS, default = "available")
    morning = serializers.BooleanField(default=True)
    day = serializers.BooleanField(default=True)
    night = serializers.BooleanField(default=True)
    payment_status = serializers.BooleanField(default=False)
    total = serializers.IntegerField(default = 0)
    
    def create(self, validated_data):
        user = validated_data.get('user')
        hall = validated_data.get('hall')
        show_date = validated_data.get('show_date')
        movie = validated_data.get('movie')
        seat = validated_data.get('seat')
        showtime = validated_data.get('showtime')
        morning = validated_data.get('morning')
        day = validated_data.get('day')
        night = validated_data.get('night')
        price = validated_data.get('price')
        
        
        if SeatAvailability.objects.filter(user = user,show_date = show_date, movie = movie, showtime = showtime,seat = seat, hall = hall,seat_status = 'pending').exists():
            myseat = SeatAvailability.objects.get(user = user.id, movie = movie.id, showtime = showtime.id,seat = seat.id, hall = hall.id,seat_status = 'pending')
            myseat.delete()
            return Response({"success":"Successfully Unreserved seat"})
        
        elif SeatAvailability.objects.filter(movie = movie,seat = seat,hall = hall, showtime = showtime, seat_status__in = ["pending","reserved"]).exists():
            raise serializers.ValidationError("Seat is Booked Already")
        
        elif BookingHistory.objects.filter(movie = movie,seats__id = seat.id,hall = hall,showtime = showtime, payment_status =True).exists():
            raise serializers.ValidationError("Seat is Booked Already")
        
        else:
            SeatAvailability.objects.create(
                user = user,
                hall = hall,
                show_date = show_date,
                movie = movie,
                seat = seat,
                showtime = showtime,
                morning = morning,
                day = day,
                night = night,
                total = price,
                seat_status = 'pending'  
            ).save()
            return Response({"success":"Resereved"})
        

# Serializer for Showing Booking Pending and Booking BookingHistory to admin 

class BookingHistorySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    hall = serializers.PrimaryKeyRelatedField(queryset=CinemaHall.objects.all(), allow_null=True, required=False)
    show_date = serializers.DateField()
    showtime = serializers.PrimaryKeyRelatedField(queryset=Showtime.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    seats = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all(), many=True)
    reservation_datetime = serializers.DateTimeField(read_only=True)
    payment_status = serializers.BooleanField(default=False)
    payment_method = serializers.CharField(max_length=50, allow_null=True, required=False)
    total = serializers.IntegerField(default=0, allow_null=True, required=False)
    


class CollectionSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset = Movie.objects.all())
    payment_amount = serializers.DecimalField(max_digits = 10, decimal_places=2)
    timestamp = serializers.DateTimeField(default = timezone.now())
    
    
    def create(self, validated_data):
        user = validated_data.get('user')
        movie = validated_data.get('movie')
        payment = validated_data.get('amount')
        
        Collection.objects.create(user = user, movie = movie, payment_amount = payment).save()
        
        

