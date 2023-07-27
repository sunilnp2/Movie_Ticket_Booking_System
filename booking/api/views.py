from booking.api.serializers import SeatSerializer, SeatAvailabilitySerializer, BookingHistorySerializer
from movie.api.serializers import MovieSerializer, ShowtimeSerializer
from cinema.api.serializers import CinemaHallSerializer
from rest_framework.views import APIView
from booking.models import Seat, SeatAvailability, BookingHistory
from rest_framework.response import Response
from rest_framework import status
from movie.models import Showtime, Movie
from cinema.models import CinemaHall
from authentication.models import Customer


class SeatAPIView(APIView):
    def get(self, request):
        seats = Seat.objects.all()
        seat_serializer = SeatSerializer(seats, many=True)
        response_data = {"Seats": seat_serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)


# Code for reserve seat pending 
class SeatReserveAPIView(APIView):
    
    def get(self, request, seat_id, movie_slug, show_id, hall_id):
        return Response({"success":"This is get method on seat availability"})
    # pass
    def post(self, request, seat_id, movie_slug, show_id, hall_id):
        user = request.user
        seat = Seat.objects.get(id=seat_id)
        # get_seat_id = Seat.objects.get(id=seat_id).id
        show_date = Showtime.objects.get(id=show_id).show_date
        sh_id = Showtime.objects.get(id=show_id)
        movie_id = Movie.objects.get(slug=movie_slug)
        hall = CinemaHall.objects.get(id=hall_id)
        price = sh_id.price

        shift = sh_id.shift
        if shift == "Morning":
            morning = False
            day = True
            night = True

        elif shift == "Day":
            morning = True
            day = False
            night = True

        elif shift == "Night":
            morning = True
            day = True
            night = False
        pass

        data = {
            'user':user.id,
            'movie': movie_id.id,
            'seat': seat.id,
            'hall': hall.id,
            'show_date': show_date,
            'showtime': sh_id.id,
            'morning': morning,
            'day': day,
            'night': night,
            'price':price,
        }
        
        serializer = SeatAvailabilitySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Done"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors)
        
        
# -------------------------------------------------  code for show booking pending user or booking histry of user ------------------------------------------------------------

class BookPenHisAPIView(APIView):
    def get(self, request):
        pending = SeatAvailability.objects.filter(payment_status = False, seat_status = 'pending')
        
        pending_serializer = SeatAvailabilitySerializer(pending, many = True)
        
        history = BookingHistory.objects.filter(payment_status = True)
        history_serializer = BookingHistorySerializer(history, many = True)
        
        response_data = {"pending":pending_serializer.data, 
                         "history":history_serializer.data}
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
    
    
    
# code for booking
class BookingAPIView(APIView):
    def get(self, request, slug,show_id, hall_id):
        user = request.user
        email = user.email
        
        movie = Movie.objects.prefetch_related('showtime_set').get(slug = slug)
        movie_serializer = MovieSerializer(movie)
        
        showtimes = movie.showtime_set.get(id = show_id)
        showtimes_serializer = ShowtimeSerializer(showtimes)
        show_date = showtimes.show_date
        
        hall = CinemaHall.objects.get(id = hall_id)
        hall_serializer = CinemaHallSerializer(hall)
        
        balance = Customer.objects.get(email = email).balance
        
        seleted_seat= SeatAvailability.objects.filter(user = request.user,hall = hall_id, show_date = show_date,showtime = show_id,movie = movie.id,  seat_status = 'pending', payment_status = False)
        try:
         total = 0 
         for p in seleted_seat:
            total = int(total) + int(p.total)
         total = total
        except Exception as e:
            print(e)
            pass
        seats = [s.seat.name for s in seleted_seat]
        
        response_data = {"movie":movie_serializer.data,"showtime":showtimes_serializer.data, "hall":hall_serializer.data,
                         "Selected_date":show_date, 
                         "Balance":balance,
                         "total":total,
                         "selected Seat":seats,}
        return Response(response_data, status=status.HTTP_200_OK)
            
            
# code for payment 

class PaymentAPIView(APIView):
    def get(self, request):
        pass
        
        
