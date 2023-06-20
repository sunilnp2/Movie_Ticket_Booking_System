from django.shortcuts import render , redirect
from booking.models import *
from cinema.views import BaseView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime

from django.http import FileResponse, HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Spacer, Paragraph, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
# Create your views here.
class Seatview(BaseView):
    # login_required = True
    def get(self,request, slug, date_id, show_id):
        self.views['first_row'] = Seat.objects.filter(seat_number__lte = 5)
        self.views['second_row'] = Seat.objects.filter(seat_number__gt=5,seat_number__lte=10)
        self.views['third_row'] = Seat.objects.filter(seat_number__gt=10,seat_number__lte=15)
        self.views['fourth_row'] = Seat.objects.filter(seat_number__gt=15,seat_number__lte=20)
        self.views['fifth_row'] = Seat.objects.filter(seat_number__gt=20,seat_number__lte=25)

        self.views['details'] = Movie.objects.get(slug = slug)
        selected_date = date_id
        showtime = show_id
        user = request.user
        try:
            seleted_seat= SeatAvailability.objects.filter(user = user,status = 'pending', payment_status = False)
            self.views['seats'] = [s.seat.name for s in seleted_seat]
            
        except Exception as e:
            print(e)
            pass
        
        self.views['dates'] = MovieDate.objects.get(id = selected_date)
        self.views['showtime'] = Showtime.objects.get(id = showtime)
        # showtime = Showtime.objects.get(date = id).id
    
        

        return render(request, 'seat.html', self.views)

@method_decorator(login_required, name='dispatch')
class ReserveView(BaseView):
    def get(self,request, seat_id, date_id, show_id, slug):
        s_id = Seat.objects.get(id = seat_id)
        d_id = MovieDate.objects.get(id = date_id)
        sh_id = Showtime.objects.get(id = show_id)
        movie_id = Movie.objects.get(slug = slug)
        price = Showtime.objects.get(id = show_id).price
        user = request.user
        user_id = user.id
        myuser = User.objects.get(id = user_id)

        shift = sh_id.shift
        if shift == "M":
            morning = False
            day = True
            night = True
        
        elif shift == "D":
            morning = True
            day = False
            night = True

        elif shift == "N":
            morning = True
            day = True
            night = False
        pass
            
        print(f"The shift is {shift}")
        if SeatAvailability.objects.filter(movie = movie_id,seat = s_id,showtime = sh_id, status__in = ["pending","reserved"]).exists():
            messages.error(request, "Movie is booked already")
            return redirect("booking:seat",slug, date_id, show_id)
        else:
            res = SeatAvailability.objects.create(user = myuser,movie = movie_id,
                                            seat = s_id,
                                             date = d_id, 
                                             showtime = sh_id,
                                             status = 'pending',
                                             morning = morning, 
                                             day = day,
                                             night = night,
                                             total = price
                                             )
            res.save()
            Seat.objects.update(status = "pending")
            messages.success(request, "Seat Reserved successfully")
            return redirect("booking:seat",slug, date_id, show_id)
        

        
class BookingView(BaseView):
    def get(self,request,slug,date_id,show_id):

        self.views['user'] = request.user
        self.views['d_id'] = MovieDate.objects.get(id = date_id)
        self.views['sh_id'] = Showtime.objects.get(id = show_id)
        self.views['movie_id'] = Movie.objects.get(slug = slug)

        seleted_seat= SeatAvailability.objects.filter(user = request.user,status = 'pending', payment_status = False)
        self.views['seats'] = [s.seat.name for s in seleted_seat]

        # seat_available = SeatAvailability.objects.get(seat = seat_id).id
        # print(seat_available)

        return render(request, 'booking.html', self.views)

    
class PaymentView(BaseView):
    def get(self, request, slug,date_id,show_id):
        movie_id = Movie.objects.get(slug = slug).id
        payment_type = request.POST.get('pay')
        user = request.user
        if SeatAvailability.objects.filter(payment_status = True,user = user, date = date_id, movie = movie_id, showtime = show_id).exists():
            messages.error(request, "Already reserved")
            return redirect('cinema:home')

        else:
            cart = SeatAvailability.objects.filter(user = user, date = date_id, movie = movie_id, showtime = show_id, status = 'pending',payment_status = False )
            my_seats = [s.seat for s in cart]
            print(my_seats)
            for c in cart:
                booking = BookingHistory.objects.create(
                    user = user,
                    movie_date = c.date,
                    showtime = c.showtime,
                    movie = c.movie,
                    reservation_datetime =  datetime.now(),
                    payment_status = True
                )
                booking.seats.set(my_seats)
                booking.save()
            SeatAvailability.objects.filter(user = user, date = date_id, movie = movie_id, showtime = show_id).update(payment_status = True, status = "reserved")

            # Code for Generate Pdf
            name = f"{user.first_name} {user.last_name}"
            email = user.email
            phone = user.phone
            address = user.address
            movie = Movie.objects.get(slug = slug)
            reserve_date = MovieDate.objects.get(id = date_id).movie_date
            showtime = Showtime.objects.get(id = show_id)
            my_seats_name = [s.seat.name for s in cart]
            str_seat = ",".join(my_seats_name)
        

            # Create a new PDF document using ReportLab
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

                # Define the ticket template styles
            styles = getSampleStyleSheet()
            title_style = styles['Heading1']
            subtitle_style = styles['Heading3']
            content_style = styles['Normal']

            # Add content to the PDF document based on the template design
            content = []

            # Add the title
            title = Paragraph('Movie Ticket', title_style)
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

            # Add spacing between elements
            content.append(Spacer(1, 12))

            # Build the PDF document and close the buffer
            doc.build(content)
            pdf_buffer.seek(0)

            # Set response headers for a downloadable PDF file
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="qfxcinema.pdf"'


            # Set the PDF content from the buffer and close the buffer
            response.write(pdf_buffer.getvalue())
            pdf_buffer.close()

            return response
        
class BookingHostoryView(BaseView):
    def get(self, request):
        user = request.user
        self.views['history'] = BookingHistory.objects.filter(user = user, payment_status = True)
        see_list = BookingHistory.objects.filter(user = user, payment_status = True)
        for s in see_list:
            seat = s.seats.all()
        my_lst = [ms.name for ms in seat]
        self.views['final_seat'] = ",".join(my_lst)
            

        return render(request, 'booking-history.html', self.views)

        
