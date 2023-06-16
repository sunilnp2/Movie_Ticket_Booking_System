from django.shortcuts import render , redirect
from booking.models import *
from cinema.views import BaseView
from django.contrib import messages
# from 
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        self.views['dates'] = Date.objects.get(id = selected_date)
        self.views['showtime'] = Showtime.objects.get(id = showtime)
        # showtime = Showtime.objects.get(date = id).id
        movie = Movie.objects.get(slug = slug).id
        # dateid = Date.objects.get(id = date_id)
        # showid = Showtime.objects.get(id = show_id)
        

        self.views['status'] =  SeatAvailability.objects.filter(movie = movie, date = date_id,showtime = show_id)
        print(len(self.views['status']))

        if (len(self.views['status'])) > 1:
            self.views['manystatus'] = self.views['status']

        else:
            self.views['onestatus'] = self.views['status']
            print(f"Length of single is {len(self.views['onestatus'])}")
            for r in self.views['onestatus']:
                val = str(r.seat)
                self.views['seatid'] = int(val)
    
        

        return render(request, 'seat.html', self.views)

# @method_decorator(login_required, name='dispatch')
class ReserveView(BaseView):
    def get(self,request, seat_id, date_id, show_id, slug):
        # print(seat_id, date_id, show_id, slug)
        # print(f"seat Nunber {seat_id}")
        # print(f"sDate Id {date_id}")
        # print(f"Showtime id {show_id}")
        # print(f"Movie Slug {slug}")
        s_id = Seat.objects.get(id = seat_id)
        d_id = Date.objects.get(id = date_id)
        sh_id = Showtime.objects.get(id = show_id)
        movie_id = Movie.objects.get(slug = slug)

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
            
        print(f"The shift is {shift}")
        if SeatAvailability.objects.filter(movie = movie_id,seat = s_id, date = d_id,showtime = sh_id).exists():
            messages.error(request, "Movie is booked already")
            return redirect("booking:seat",slug, date_id, show_id)
        else:
            res = SeatAvailability.objects.create(movie = movie_id,
                                            seat = s_id,
                                             date = d_id, 
                                             showtime = sh_id,
                                             status = 'pending',
                                             morning = morning, 
                                             day = day,
                                             night = night
                                             
                                             )
            res.save()
            Seat.objects.update(status = "pending")
            messages.success(request, "Seat Reserved successfully")
            return redirect("booking:seat",slug, date_id, show_id)
        
class BookingView(BaseView):
    def get(self, request):
        # seat_available = SeatAvailability.objects.get(seat = seat_id).id
        # print(seat_available)

        return render(request, 'booking.html')
    
        
