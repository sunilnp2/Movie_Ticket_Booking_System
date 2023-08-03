# serializer for Seat View
from rest_framework import serializers
from booking.models import SEAT_STATUS, SeatAvailability, Seat, BookingHistory, Collection
from authentication.models import User, Customer
from movie.models import Movie, Showtime
from cinema.models import CinemaHall
from rest_framework.response import Response
from django.utils import timezone

# from authentication.api.serializers import CustomerSerializer
from django.db import transaction

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
# -----------------------------One Option 1------------------------------
'''
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
        


class BookingHistorySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    hall = serializers.PrimaryKeyRelatedField(queryset=CinemaHall.objects.all(), allow_null=True, required=False)
    show_date = serializers.DateField()
    showtime = serializers.PrimaryKeyRelatedField(queryset=Showtime.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    seats = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all(), many=True)
    reservation_datetime = serializers.DateTimeField(default = timezone.now())
    payment_status = serializers.BooleanField(default=False)
    payment_method = serializers.CharField(max_length=50, allow_null=True, required=False)
    total = serializers.IntegerField(default=0, allow_null=True, required=False)


    
    def create(self, validated_data):
        user = validated_data.get('user')
        hall = validated_data.get('hall')
        show_date = validated_data.get('show_date')
        showtime = validated_data.get('showtime')
        movie = validated_data.get('movie')
        paymethod_method = validated_data.get('pay_method')
        total = validated_data.get('total')
    
        seats = validated_data.get('user')
        
        BookingHistory.objects.create(
            user = user,
            hall = hall,
            show_date = show_date, 
            showtime = showtime,
            movie = movie,
            payment_status = True,
            paymethod_method = paymethod_method,
            total = total,
            seats = seats
        )

        '''

# -----------------------------Two Option 2------------------------------
class CollectionSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset = Movie.objects.all())
    payment_amount = serializers.DecimalField(max_digits = 10, decimal_places=2)
    timestamp = serializers.DateTimeField(default = timezone.now())
    
    
    def create(self, validated_data):
        Collection.objects.create(**validated_data)


class BookingHistorySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    hall = serializers.PrimaryKeyRelatedField(queryset=CinemaHall.objects.all(), allow_null=True, required=False)
    show_date = serializers.DateField()
    showtime = serializers.PrimaryKeyRelatedField(queryset=Showtime.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    seats = serializers.PrimaryKeyRelatedField(many=True, queryset=Seat.objects.all(), required=False)
    reservation_datetime = serializers.DateTimeField(default = timezone.now())
    payment_status = serializers.BooleanField(default=False)
    payment_method = serializers.CharField(max_length=50, allow_null=True, required=False)
    total = serializers.IntegerField(default=0, allow_null=True, required=False)
    collection = CollectionSerializer()


    def create(self, validated_data):
        collection_data = validated_data.pop('collection')
        seats_data = validated_data.pop('seats', [])
        # customer_email  = User.objects.get(id = validated_data.get('user')).email
        balance = Customer.objects.get(email = validated_data.get('user')).balance


        

        try:
            if transaction.atomic():
                Collection.objects.create(**collection_data)



                # for booking history

                booking_history_instance = BookingHistory.objects.create(
                    **validated_data
                )
                booking_history_instance.payment_status = True
                booking_history_instance.save()
                booking_history_instance.seats.set(seats_data)

                SeatAvailability.objects.filter(user = validated_data.get('user'),
                                                hall = validated_data.get('hall'),
                                                show_date = validated_data.get('show_date'),
                                                movie = validated_data.get('movie'),
                                                showtime = validated_data.get('showtime'),
                                                payment_status = False).update(payment_status = True, seat_status = "reserved")
                

                Customer.objects.filter(email = validated_data.get('user')).update(balance = balance - validated_data.get('total'))
                return booking_history_instance
        except Exception as e:
            print(e)
            
        