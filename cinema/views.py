from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from movie.models import *
from utils.forms import FilterMovieForm
from django.db.models import *
from booking.models import Seat

# # Create your views here.

class BaseView(View):
    views = {}
    views['showing'] = Movie.objects.filter(movie_status = "showing")
    views['coming'] = Movie.objects.filter(movie_status = "comingsoon")
    

class HomeView(BaseView):
    def get(self,request):
        fm = FilterMovieForm(request.GET)
        showing = Movie.objects.filter(movie_status = "showing")
        upcoming = Movie.objects.filter(movie_status = "comingsoon")
        
        recommended_movies = Movie.objects.annotate(like_count=Count('like')).filter(like_count__gt=2, like__like__isnull=False)
        return render(
            request,'index.html', 
            context={'showing':showing, 'coming':upcoming,'fm':fm, 'recom':recommended_movies})
    
