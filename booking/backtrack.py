from booking.models import SeatAvailability, Showtime,Seat
from django.shortcuts import render , redirect
from booking.models import *
from cinema.views import BaseView
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
from django.http import FileResponse, HttpResponse, JsonResponse
from io import BytesIO
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph, Spacer, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet
from django.core.mail import EmailMessage
from django.conf import settings
from authentication.models import Customer

def find_best_seat(cinema_hall, num_seats_required):
    # Create a list to store unique seat scores along with their positions
    seat_scores = []
    for row in range(len(cinema_hall)):
        for col in range(len(cinema_hall[0])):
            seat = cinema_hall[row][col]
            seat.score = calculate_seat_score(seat)

            seat_scores.append((row, col, seat.score))
    sorted_seats = sorted(seat_scores, key=lambda x: x[2], reverse=True)

    available_seats = [(row, col) for row, col, score in sorted_seats if cinema_hall[row][col] == 'available']

    # Return the recommended seats
    return available_seats[:num_seats_required]


def calculate_seat_score(seat):
    # Calculate Seat Score based on Seat Characteristics
    print(f"The seat is {seat}")
    # seat = Seat.objects.get(id = seat)
    seat_score = (
        seat.seat_score +
        seat.screen_visibility
    )
    print(seat_score)
    return seat_score


def recommend_using_backtrack(show_id, hall_id, num_seats_required):
    # Get the queryset of Seat objects
    seats_queryset = Seat.objects.all()
    showtime = Showtime.objects.select_related('movie').get(id = show_id)
    movie = showtime.movie.id
    show_date = showtime.show_date



    # Create a list to store unique seat scores along with their positions
    seat_scores = []

    # Iterate through the seats in the queryset
    for seat in seats_queryset:
        # Filter the SeatAvailability objects for the specific seat, showtime, and date with 'reserved' status
        reserved_seats = SeatAvailability.objects.filter(
            seat=seat,
            showtime_id=show_id,
            hall_id=hall_id,
            movie = movie,
            show_date = show_date,
            seat_status__in = ('reserved', 'pending')
        )

        # If no reservations found for the specific seat, calculate the seat score
        if not reserved_seats.exists():
            seat_score = calculate_seat_score(seat)
            # Add the seat and its score to the list
            seat_scores.append((seat, seat_score))

    # Sort seats by score (descending order, higher scores first)
    sorted_seats = sorted(seat_scores, key=lambda x: x[1], reverse=True)

    # Return the recommended seats
    recommended_seats = [seat for seat, seat_score in sorted_seats]

    return recommended_seats[:num_seats_required]


#------------------------------------ Backtracking Algorithm for Reserve seat ----------------------------------------------------
# ----------------------------------Seat Booking with BackTracking Algorithm-------------------------------------------------------


def is_valid_seat_combination(seats_queryset, num_seats_required, current_reservation=[], valid_reservations=[]):
    if len(current_reservation) == num_seats_required:
        # Base case: Valid combination found, add to list of valid reservations
        valid_reservations.append(current_reservation)
        return

    for seat in seats_queryset:
        if seat.seat_status == 'available':
            # Choose the seat and mark it as reserved ('pending')
            seat.seat_status = 'pending'
            seat_reservation_backtrack(seats_queryset, num_seats_required, current_reservation + [seat], valid_reservations)
            # Backtrack: Restore the seat status to 'available' to explore other possibilities
            seat.seat_status = 'available'

    return True

def seat_reservation_backtrack(seats, num_seats_required, current_reservation=[], start_index=0):
    if len(current_reservation) == num_seats_required:
        # Base case: Valid combination found, return it
        if is_valid_seat_combination(current_reservation):
            return current_reservation.copy()
        return []

    for i in range(start_index, len(seats)):
        seat = seats[i]
        if seat.seat_status == 'available':
            # Choose the seat and mark it as reserved
            seat.seat_status = 'pending'
            result = seat_reservation_backtrack(seats, num_seats_required, current_reservation + [seat], i + 1)
            if result:
                return result
            seat.seat_status = 'available'

    return seat



# views.py

@method_decorator(login_required, name='dispatch')
class ReserveView(BaseView):
    def post(self, request, seat_id, show_id, slug, hall_id):
        user = request.user
        s_id = Seat.objects.get(id = seat_id)
        get_seat_id = Seat.objects.get(id = seat_id).id
        show_date = Showtime.objects.get(id = show_id).show_date
        sh_id = Showtime.objects.get(id = show_id)
        movie_id = Movie.objects.get(slug = slug)
        hall = CinemaHall.objects.get(id = hall_id)
        price = Showtime.objects.get(id = show_id).price
        user = request.user
        user_id = user.id
        myuser = User.objects.get(id = user_id)

        # Get the existing seat status for the selected showtime, hall, and date
        seats = SeatAvailability.objects.filter(showtime_id=show_id, hall_id=hall_id, date_id=show_date)

        # Check if the selected seat is available
        selected_seat = Seat.objects.get(id=seat_id)
        if selected_seat.seat_status == 'available':
            # The seat is available, proceed with reservation
            selected_seat.seat_status = 'reserved'
            selected_seat.save()

            # Use the backtracking algorithm to find a valid reservation
            num_seats_required = 1  # Adjust this based on your requirement
            valid_reservation = seat_reservation_backtrack(seats, num_seats_required)
            shift = sh_id.shift
            if shift == "Morning":
                morning, day, night = False, True, True
            elif shift == "Day":
                morning, day, night = True, False, True
            elif shift == "Night":
                morning, day, night = True, True, False

            if valid_reservation:
                # Handle the reservation logic (create SeatAvailability objects, update totals, etc.)
                res = SeatAvailability.objects.create(user = myuser,movie = movie_id,
                                            seat = s_id,
                                            hall = hall,
                                             show_date = show_date, 
                                             showtime = sh_id,
                                             seat_status = 'pending',
                                             morning = morning, 
                                             day = day,
                                             night = night,
                                             total = price
                                             )
                res.save()
                Seat.objects.update(seat_status = "pending")
                
                res_data = {
                    "success": "Seat reserved successfully",
                    "slug": slug,
                    "date_id": show_date,
                    "show_id": show_id,
                    "hall_id": hall_id,
                    "seats": [seat.seat.name for seat in valid_reservation],
                }
                response = JsonResponse(res_data)
                response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
                return response
            else:
                # No valid reservation found
                # Handle this case accordingly
                pass

        else:
            # The seat is not available for reservation
            res_data = {
                "error": "Seat is not available for reservation",
                "slug": slug,
                "date_id": show_date,
                "show_id": show_id,
                "hall_id": hall_id,
            }
            response = JsonResponse(res_data)
            response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
            return response
