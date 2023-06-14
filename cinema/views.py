from django.shortcuts import render, redirect
from django.views import View
from cinema.forms import SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from cinema.models import *
from datetime import date
from django.http import HttpResponse
# Create your views here.


from .tokens import account_activation_token

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()

        messages.success(request, "Thank you for your email confirmation you can login your account.")
        return redirect('cinema:login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("email-activate.html", {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f' Dear {user.first_name}.Go to your email {to_email} and verify your email \
                If not found Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

class BaseView(View):
    views = {}
    views['showing'] = Movie.objects.filter(status = "showing")
    views['coming'] = Movie.objects.filter(status = "comingsoon")


class HomeView(BaseView):
    def get(self,request):
        user = get_user_model()
        name = user.first_name

        return render(request,'index.html', self.views)
    

class MovieView(BaseView):
    def get(self, request):
        return render(request, 'movie.html', self.views)
    

class MovieSearchView(BaseView):
    def get(self,request):
        search = request.GET.get('search', None)
        if search:
            self.views['search'] = Movie.objects.filter(name__icontains = search)

            return render(request, 'movie-search.html', self.views)
        else:
            return redirect('cinema:movie')
        

class MovieDetailView(BaseView):
    def get(self, request, slug):
        self.views['details'] = Movie.objects.get(slug = slug)

        # code for showing dates
        self.views['dates'] = Date.objects.filter(date__gte = date.today())
        
        # self.views['formatted_date'] = mydate.strftime('%b, %b %d, %Y')

        a = self.views['details']
        print(a.name)
        print(a.status)
       
        return render(request, 'movie-detail.html', self.views)
    

class MovieShowTimeView(BaseView):
    def get(self, request, id, slug):

        self.views['details'] = Movie.objects.get(slug = slug)
        self.views['dates'] = Date.objects.get(id = id)
        print(id)

        # selected_date = Date.objects.get(id = id).date
        self.views['showtimes'] = Showtime.objects.filter(date = id)

        return render(request, 'movie-showtime.html', self.views)
        

    
class Seatview(BaseView):

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
        print(selected_date, showtime)

        return render(request, 'seat.html', self.views)

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
            return redirect("cinema:seat",slug, date_id, show_id)
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
            return redirect("cinema:seat",slug, date_id, show_id)
        




    
class BookingView(BaseView):
    def get(self, request, seat_id):
        seat_available = SeatAvailability.objects.get(seat = seat_id).id
        # print(seat_available)

        return render(request, 'booking.html')
    





    

class LoginView(BaseView):
    def get(self,request):
        self.views['fm'] = LoginForm()
        return render(request, 'login.html', self.views)
    
    def post(self,request):

        # fm = LoginForm(request.POST)
        # if fm.is_valid():
        #     email = fm.cleaned_data['email']
        #     pw = fm.cleaned_data['password1']

        #     user = authenticate(email = email, password = pw)
        #     if user is not None:
        #         login(request,user)
        #         messages.success(request, "You are login successfully")
        #         return redirect('cinema:home')
        
        # return render(request, 'login.html', {'fm': fm})
        email = request.POST.get('email')
        pw = request.POST.get('password')
        if not email:
            messages.error(request,"Username required")
        if not pw:
            messages.error(request,"Username required")
        user = authenticate(email = email, password = pw)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully")
            return redirect('cinema:home')
        else:
            messages.error(request, "Enter Correct password")
        return render(request, 'login.html')


class SignupView(BaseView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get(request, *args, **kwargs)
        elif request.method == 'POST':
            return self.post(request, *args, **kwargs)
        else:
            return HttpResponse(['GET', 'POST']) 
        
    def get(self,request):
        self.views['fm'] = SignupForm()
        return render(request, 'signup.html', self.views)

    def post(self,request):
        fm = SignupForm(request.POST)
        if fm.is_valid():
            user = fm.save(commit=False)
            user.email_verified=False
            user.save()
            activateEmail(request, user, fm.cleaned_data.get('email'))
            fm.save()
            return redirect('cinema:home')
        return render(request, 'signup.html', {'fm': fm})


        
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Log Out success")
        return redirect('cinema:home')