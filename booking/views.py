from django.shortcuts import render , redirect
from booking.models import *
from cinema.views import BaseView
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
from django.http import FileResponse, HttpResponse
from io import BytesIO
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph, Spacer, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet
from django.core.mail import EmailMessage
from django.conf import settings
from authentication.models import Customer
    

from utils.tasks import send_ticket
# Create your views here.
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



@method_decorator(login_required, name='dispatch')
class Seatview(BaseView):
    """ 
    This View Shows The reserved and vacant seats of selected cinema hall , movie and showtime.
    """
    def get(self,request, slug, show_id, hall_id):
        show_date = Showtime.objects.get(id = show_id).show_date
        self.views['first_row'] = Seat.objects.filter(seat_number__lte = 5)
        self.views['second_row'] = Seat.objects.filter(seat_number__gt=5,seat_number__lte=10)
        self.views['third_row'] = Seat.objects.filter(seat_number__gt=10,seat_number__lte=15)
        self.views['fourth_row'] = Seat.objects.filter(seat_number__gt=15,seat_number__lte=20)
        self.views['fifth_row'] = Seat.objects.filter(seat_number__gt=20,seat_number__lte=25)
        
        # Get the queryset for available seats
        num_seats_required = 1

        # Calculate the recommended seats using the seat recommendation algorithm
        recommended_seats = recommend_using_backtrack(show_id, hall_id, num_seats_required)
        print(f"The recommended Seat is{recommended_seats}")


        self.views['recommended_seat'] = recommended_seats
        self.views['details'] = Movie.objects.get(slug = slug)
        movie_id = self.views['details'].id
        user = request.user
        self.views['booked_seats'] = SeatAvailability.objects.filter(
            user=request.user,
            seat_status='pending',
            hall=hall_id,
            payment_status=False,
            movie=movie_id,
            showtime=show_id,
            show_date=Showtime.objects.get(id = show_id).show_date
        ).values_list('seat__name', flat=True)
        try:
            seleted_seat= SeatAvailability.objects.filter(user = user, seat_status = 'pending',hall = hall_id,payment_status = False, movie = movie_id, showtime = show_id , show_date = show_date)
            seat = [s.seat.name for s in seleted_seat]
            
            self.views['seats'] = ",".join(seat)
            
        except Exception as e:
            print(e)
            pass
        seleted_seat= SeatAvailability.objects.filter(user = user, seat_status = 'pending',hall = hall_id,payment_status = False, movie = movie_id, showtime = show_id , show_date = show_date)
        # , show_date = show_id,movie = movie_id,showtime = show_id 
        total = 0 
        for p in seleted_seat:
            total += p.total
        self.views['total'] = total
        self.views['hall_name'] = CinemaHall.objects.get(id = hall_id)
        self.views['hall_id'] = hall_id
        self.views['dates'] = Showtime.objects.get(id = show_id).show_date
        self.views['showtime'] = Showtime.objects.get(id = show_id)
        

        return render(request, 'seat.html', self.views)
    

@method_decorator(login_required, name='dispatch')
class ReserveView(BaseView):
    """
    When user try to reserved seat This view check the Seat Status 
    If seat is vacant it will reserved the selected seat with user id
    using Jquery and Ajax
    
    """
    def post(self,request, seat_id, show_id, slug, hall_id):
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
        # num_seats_required = 1
        # recommended_seats = recommend_using_backtrack(show_id, hall_id, num_seats_required)
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
            
        user = request.user
        print(f"The shift is {shift}")
        if SeatAvailability.objects.filter(user = user, movie = movie_id, showtime = sh_id,seat = s_id, hall = hall_id,seat_status = 'pending').exists():
            myseat = SeatAvailability.objects.get(user = user, movie = movie_id, showtime = sh_id,seat = s_id, hall = hall_id,seat_status = 'pending')
            myseat.delete()
            try:
                seleted_seat= SeatAvailability.objects.filter(user = user, seat_status = 'pending',hall = hall_id,payment_status = False, movie = movie_id, showtime = show_id , show_date = show_date)
                seats = [s.seat.name for s in seleted_seat]
            
            except Exception as e:
                print(e)
                pass
            seleted_seat= SeatAvailability.objects.filter(user = user, seat_status = 'pending',hall = hall_id,payment_status = False, movie = movie_id, showtime = show_id , show_date = show_date)
            total = 0 
            for p in seleted_seat:
                total += p.total
            res_data = {"success":"Seat Un reserved", "slug":slug, "date_id":show_date, "show_id":show_id, "hall_id":hall_id, "total":total, "seat":seats}
            response = JsonResponse(res_data)
            response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
            return response
        
        elif SeatAvailability.objects.filter(movie = movie_id,seat = s_id,hall = hall_id, showtime = show_id, seat_status__in = ["pending","reserved"]).exists():
            res_data = {"success":"Movie is booked Already", "slug":slug, "date_id":show_date, "show_id":show_id, "hall_id":hall_id}
            response = JsonResponse(res_data)
            response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
            return response
        
        elif BookingHistory.objects.filter(movie = movie_id,seats__id = get_seat_id,hall = hall_id,showtime = sh_id, payment_status =True).exists():
            res_data = {"success":"Seat reserved Already", "slug":slug, "date_id":show_date, "show_id":show_id, "hall_id":hall_id}
            response = JsonResponse(res_data)
            response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
            return response
    
        else:
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
            try:
                seleted_seat= SeatAvailability.objects.filter(user = user, seat_status = 'pending',hall = hall_id,payment_status = False, movie = movie_id, showtime = show_id , show_date = show_date)
                seats = [s.seat.name for s in seleted_seat]
            
            except Exception as e:
                print(e)
                pass
            seleted_seat= SeatAvailability.objects.filter(user = user, seat_status = 'pending',hall = hall_id,payment_status = False, movie = movie_id, showtime = show_id , show_date = show_date)
            total = 0 
            for p in seleted_seat:
                total += p.total
            res_data = {"success":"Seat reserved successfully", "slug":slug, "date_id":show_date, "show_id":show_id, "hall_id":hall_id, "total":total, "seat":seats}
            response = JsonResponse(res_data)
            response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
            return response 
        
        


        

        
class BookingView(BaseView):
    """
    This view shows the all booking information of user with Selected Cinema hall, Selected date
    Selected showtime and Selected seats accordingly.
    """
    def get(self,request,slug,show_id, hall_id):
        self.views['user'] = request.user
        email = self.views['user'].email
        self.views['balance'] = Customer.objects.get(email = email).balance
        self.views['show_date'] = Showtime.objects.get(id = show_id).show_date
        self.views['sh_id'] = Showtime.objects.get(id = show_id)
        self.views['movie_id'] = Movie.objects.get(slug = slug)
        m_id= Movie.objects.get(slug = slug).id
        self.views['hall'] = CinemaHall.objects.get(id = hall_id)

        seleted_seat= SeatAvailability.objects.filter(user = request.user,hall = hall_id, show_date = self.views['show_date'],showtime = show_id,movie = m_id,  seat_status = 'pending', payment_status = False)
        total = 0 
        for p in seleted_seat:
            total += p.total
        self.views['total'] = total
        self.views['seats'] = [s.seat.name for s in seleted_seat]
        return render(request, 'booking.html', self.views)

    
class PaymentView(BaseView):
    """
    This views verify the user booking and reserve the seat with current user id 
    and generate and provide pdf of selected seat to user
    
    """
    def get(self, request, slug,show_id, hall_id):
        if request.method == 'POST':
            payment_type = request.POST.get('pay')
        movie_id = Movie.objects.get(slug = slug).id
        user = request.user 
        my_user_id = user.id
        user_id = user.email 
        movie_obj = Movie.objects.get(slug = slug)
        customer = Customer.objects.get(email = user_id)
        balance = Customer.objects.get(email = user_id).balance
        print(balance)
        show_date = Showtime.objects.get(id = show_id).show_date
        if SeatAvailability.objects.filter(user = user,hall = hall_id, show_date = show_date, movie = movie_id, showtime = show_id, seat_status = 'pending',payment_status = False).exists():
            cart = SeatAvailability.objects.filter(user = user,hall = hall_id, show_date = show_date, movie = movie_id, showtime = show_id, seat_status = 'pending',payment_status = False )
            total = 0
            for c in cart:
                total += c.total
            print(total)

            if balance > total:

            
                my_seats = [s.seat for s in cart]
                print(my_seats)
                booking = BookingHistory.objects.create(
                user = user,
                hall = CinemaHall.objects.get(id = hall_id),
                show_date = cart[0].show_date,
                showtime = cart[0].showtime,
                movie = cart[0].movie,
                reservation_datetime =  datetime.now(),
                payment_status = True, 
                total =total) 
                
                booking.seats.set(my_seats)
                booking.save()
                balance = balance - total
                # cart.delete()
                SeatAvailability.objects.filter(user = user,hall = hall_id, show_date = show_date, movie = movie_id, showtime = show_id).update(payment_status = True, seat_status = "reserved")
                Customer.objects.filter(email = user_id).update(email = user_id, balance = balance)
                
                # code for adding collection 
                Collection(user = user, movie = movie_obj,payment_amount = total).save()

                # Code for Generate Pdf
                name = f"{user.first_name} {user.last_name}"
                email = user.email
                phone = user.phone
                address = user.address
                movie = Movie.objects.get(slug = slug)
                reserve_date = Showtime.objects.get(id = show_id).show_date
                showtime = Showtime.objects.get(id = show_id)
                mycart = SeatAvailability.objects.filter(user = user,hall = hall_id, show_date = show_date, movie = movie_id, showtime = show_id, payment_status = True)
                my_seats_name = [s.seat.name for s in mycart]
                print(f" The seat name is {my_seats_name}")
                # str_seat = ",".join(my_seats_name)

    

                # Create a new PDF document using ReportLab
                pdf_buffer = BytesIO()

                # set the height and width of pdf 
                width = 500
                height = 300
                # Define the page background color and border
            
                doc = SimpleDocTemplate(pdf_buffer, pagesize=(width, height))

                    # Define the ticket template styles
                styles = getSampleStyleSheet()
                title_style = styles['Heading1']
                subtitle_style = styles['Heading3']
                content_style = styles['Normal']

                # Add content to the PDF document based on the template design
                content = []

                # Add the title
                title = Paragraph('QFX Movie Ticket', title_style)
                content.append(title)

                # Add customer details
                customer_info = Paragraph(f'Name: {name} \n Phone : {phone} \n email : {email} \n Address : {address}', content_style)
                content.append(customer_info)

                # Add Reserve Date information
                showtime_info = Paragraph(f'Date: {reserve_date}', content_style)
                content.append(showtime_info)

                # Add Showtime
                seat_info = Paragraph(f'Showtime: {showtime.shift} Time: {showtime.start_time}-{showtime.end_time}', content_style)
                content.append(seat_info)

                # Add seat details
                seat_info = Paragraph(f'Movie: {movie}', content_style)
                content.append(seat_info)

                # Add seat details
                seat_info = Paragraph(f'Selected Seat: {my_seats_name}', content_style)
                content.append(seat_info)

                # Add Price details
                seat_info = Paragraph(f'Price: {showtime.price}', content_style)
                content.append(seat_info)
                
                # Add Price details
                seat_info = Paragraph(f'Thank You', content_style)
                content.append(seat_info)

                # Add spacing between elements
                content.append(Spacer(1, 12))

                # Build the PDF document and close the buffer
                doc.build(content)
                pdf_buffer.seek(0)
                
                # Set response headers for a downloadable PDF file
                # response = HttpResponse(content_type='application/pdf')
                # response['Content-Disposition'] = 'attachment; filename="qfxcinema.pdf"'

                   # Create the EmailMessage object with the PDF attachment
                # email = EmailMessage(subject, message, from_email, recipient_list)
                # email.attach('qfxcinema.pdf', pdf_buffer.getvalue(), 'application/pdf')
                pdf = ('qfxcinema.pdf', pdf_buffer.getvalue(), 'application/pdf')

                # Send the email
                # email.send()

                # Set the PDF content from the buffer and close the buffer
                # response.write(pdf_buffer.getvalue())
                send_ticket.delay(my_user_id, pdf)
                pdf_buffer.close()
                # return resposnse
                
                messages.success(request,"Ticket Booked Successfully GO to your email to check pdf")
                return redirect('cinema:home')
            else:
                messages.error(request, "You don't have enough balance please Load balance")
                return redirect('cinema:home')
        
            
        
        elif SeatAvailability.objects.filter(user = user, show_date = show_date, movie = movie_id, showtime = show_id, seat_status = "reserved", payment_status = True).exists():
            messages.error(request, "Already reserved")
            return redirect('cinema:home')
        
        messages.error(request,"Select one seat")
        return redirect('cinema:home')
    
    
class GetPdfView(BaseView):
    """
    This view provide a pdf of booking history of user
    """
    def get(self, request, slug, hall_id, show_id):
        # Code for Generate Pdf
            user = request.user
            name = f"{user.first_name} {user.last_name}"
            email = user.email
            phone = user.phone
            address = user.address
            movie = Movie.objects.get(slug = slug)
            reserve_date = Showtime.objects.get(id = show_id).show_date
            showtime = Showtime.objects.get(id = show_id)
            mycart = BookingHistory.objects.filter(user = user,hall = hall_id, show_date = reserve_date, movie = movie.id, showtime = show_id, payment_status = True)
            my_seats_name = [s.seats.name for s in mycart]
            print(f" The seat name is {my_seats_name}")
            # str_seat = ",".join(my_seats_name)
        

            # Create a new PDF document using ReportLab
            pdf_buffer = BytesIO()

            # set the height and width of pdf 
            width = 500
            height = 300
            # Define the page background color and border
         
            doc = SimpleDocTemplate(pdf_buffer, pagesize=(width, height))

                # Define the ticket template styles
            styles = getSampleStyleSheet()
            title_style = styles['Heading1']
            subtitle_style = styles['Heading3']
            content_style = styles['Normal']

            # Add content to the PDF document based on the template design
            content = []

            # Add the title
            title = Paragraph('QFX Movie Ticket', title_style)
            content.append(title)

            # Add customer details
            customer_info = Paragraph(f'Name: {name} \n Phone : {phone} \n email : {email} \n Address : {address}', content_style)
            content.append(customer_info)

            # Add Reserve Date information
            showtime_info = Paragraph(f'Date: {reserve_date}', content_style)
            content.append(showtime_info)

            # Add Showtime
            seat_info = Paragraph(f'Showtime: {showtime.shift} Time: {showtime.start_time}-{showtime.end_time}', content_style)
            content.append(seat_info)

            # Add seat details
            seat_info = Paragraph(f'Movie: {movie}', content_style)
            content.append(seat_info)

            # Add seat details
            seat_info = Paragraph(f'Selected Seat: {my_seats_name}', content_style)
            content.append(seat_info)

            # Add Price details
            seat_info = Paragraph(f'Price: {showtime.price}', content_style)
            content.append(seat_info)
            
            # Add Price details
            seat_info = Paragraph(f'Thank You', content_style)
            content.append(seat_info)

            # Add spacing between elements
            content.append(Spacer(1, 12))

            # Build the PDF document and close the buffer
            doc.build(content)
            pdf_buffer.seek(0)
            
            # Set the PDF content from the buffer and close the buffer
            pdf_content = pdf_buffer.getvalue()
            pdf_buffer.close()
          
            
              # Create an email message
            email = EmailMessage(
                'Movie Ticket',
                'Please find attached your movie ticket.',
                settings.EMAIL_HOST_USER,
                [email],
            )

            # Attach the PDF to the email
            email.attach('qfxcinema.pdf', pdf_content, 'application/pdf')

            # Send the email
            email.send()
            
              # Set response headers for a downloadable PDF file
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="qfxcinema.pdf"'
            response.write(pdf_content)


         

            return response
        
class BookingHostoryView(BaseView):
    """_summary_

    This views shows the All booking history of user in history template
    """
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            self.views['history'] = BookingHistory.objects.filter(user = user, payment_status = True)
            see_list = BookingHistory.objects.filter(user = user, payment_status = True)
            seat = []
            for s in see_list:
                seat += list(s.seats.all())
            my_lst = [ms.name for ms in seat]
            self.views['final_seat'] =  ",".join(my_lst)
            

            return render(request, 'booking-history.html', self.views)
        messages.error(request, "You need to login first")
        return redirect('authentication:login')
    

class AdminBookingView(BaseView):
    """

    This views shows the all pending booking history and booking history of user 
    and manage the booking by user
    """
    def get(self, request):
        see_list = BookingHistory.objects.filter(payment_status = True)
        seat = []
        for s in see_list:
                seat += list(s.seats.all())
        my_lst = [ms.name for ms in seat]
        self.views['final_seat'] =  ",".join(my_lst)
        self.views['seatreserve'] = SeatAvailability.objects.filter(seat_status = "pending", payment_status = False)
        self.views['history'] = BookingHistory.objects.filter(payment_status = True)
        return render(request, 'booking-list-admin.html', self.views)

class DeletePendingView(View):
    """
    This view is used for filter the pending booking by user
    """
    def post(self, request, id):
        seat = SeatAvailability.objects.get(id = id)
        seat.delete()
        return JsonResponse({"message":"Delete Successfully"})
    
class BookingHistoryDeleteView(View):
    """_summary_

    This view is used for filter the  booking history of user.
    """
    def post(self, request, id):
        history = BookingHistory.objects.get(id = id)
        history.delete()
        # messages.error(request,"History Delete successcully")
        return JsonResponse({'message':"Successfully deleted"})
    
# Delete with Jquery and Ajax 
from django.http import JsonResponse

class DeleteBookingView(View):
    def post(self, request):
        booking_id = request.POST.get('booking-id')
        try:
            booking = BookingHistory.objects.get(id=booking_id)
            booking.delete()
            return JsonResponse({'success': 'Booking deleted successfully.'})
        except BookingHistory.DoesNotExist:
            return JsonResponse({'error': 'Booking not found.'})

        



# ----------------------------------Seat Booking with BackTracking Algorithm-------------------------------------------------------

def seat_reservation_backtrack(seats_queryset, num_seats_required, current_reservation=[], valid_reservations=[]):
    if len(current_reservation) == num_seats_required:
        # Base case: Valid combination found, add to list of valid reservations
        valid_reservations.append(current_reservation)
        return

    for seat in seats_queryset:
        if seat.seat_status == 'available':
            # Choose the seat and mark it as reserved ('pending')
            seat.seat_status = 'pending'
            # Recursive call to explore further
            seat_reservation_backtrack(seats_queryset, num_seats_required, current_reservation + [seat], valid_reservations)
            # Backtrack: Restore the seat status to 'available' to explore other possibilities
            seat.seat_status = 'available'

class ReserveView(BaseView):
    def post(self, request, seat_id, show_id, slug, hall_id):
        # ... (your existing code)

        # Get the existing seat status for the selected showtime, hall, and date
        seats_queryset = SeatAvailability.objects.filter(showtime_id=show_id, hall_id=hall_id, date_id=show_date)

        # Check if the selected seat is available
        selected_seat = Seat.objects.get(id=seat_id)
        if selected_seat.seat_status == 'available':
            # The seat is available, proceed with reservation
            selected_seat.seat_status = 'reserved'
            selected_seat.save()

            # Calculate the old price if the user already has a reservation
            old_reservation = SeatAvailability.objects.filter(user=myuser, show_date=show_date, showtime=sh_id, seat_status='reserved')
            old_total = 0
            if old_reservation.exists():
                old_total = old_reservation.aggregate(Sum('total'))['total__sum']

            # Calculate the new total price (price of the showtime for one seat reservation)
            new_total = Showtime.objects.get(id=show_id).price

            # Create a new SeatAvailability object to reserve the seat
            seat_availability = SeatAvailability.objects.create(
                user=myuser,
                movie=movie_id,
                seat=selected_seat,
                hall=hall,
                show_date=show_date,
                showtime=sh_id,
                seat_status='reserved',
                total=new_total
            )

            # Calculate the final total price (old total + new total)
            final_total = old_total + new_total

            # ...

            # Return the response using JsonResponse
            res_data = {
                "success": "Seat reserved successfully",
                "slug": slug,
                "date_id": show_date,
                "show_id": show_id,
                "hall_id": hall_id,
                "total": final_total,
                "seats": seats,  # You need to set 'seats' based on the selected seats
            }
            response = JsonResponse(res_data)
            response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
            return response
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
