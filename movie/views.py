from django.shortcuts import render, redirect , get_object_or_404
from cinema.views import BaseView
from movie.models import *
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.forms import FilterMovieForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from utils.form.search.search_movies import SearchForm
from django.contrib import messages

# Create your views here.


class MovieView(BaseView):
    """"""
    def get(self, request):
        """ 
        This views Display the currently showing and upcoming movie.
        """
        return render(request, 'movie.html', self.views)


class MovieSearchView(BaseView):
    def get(self, request):
        """
        This views gets the user search data and return matching movie.
        """
        sf = SearchForm({"search": request.GET.get('search', '')})
        if sf.is_valid():
            movie_qs = sf.filter_movie()
            return render(request, 'movie-search.html',context = {'search':movie_qs})
        else:
            movie_qs = []
            return render(request, 'movie-search.html',context = {'search':movie_qs})
        
       

class MovieFilterView(BaseView):
    def get(self, request):
        """
        This views get the user filter data like Movie Date , Language, Genre Filter and return and matching movie.
        """
        fm = FilterMovieForm(request.GET)
        if fm.is_valid():
            self.views['mov'] = fm.filter_movie()
            return render(request, 'movie-search.html', self.views)
        else:
            return redirect('conema:home')

class MovieDetailView(BaseView):
    def get(self, request, slug):
        """
        This views gets the movie slug and show the details of the movie.
        User can like and unlike in this view
        """
        self.views['details'] = Movie.objects.prefetch_related('like_set').get(slug=slug)
        showtime_dates = Showtime.objects.filter(show_date__gte=date.today() , movie = self.views['details'].id)
        self.views['dates'] = showtime_dates.order_by('show_date').distinct('show_date').values('show_date', 'pk')
        
        
        self.views['hall_name'] = None
        self.views['selected_date'] = None
        
        movie_id = self.views['details'].id
        try:
            
            like = self.views['details'].like_set.filter(movie=movie_id).order_by('liked_at').last()
            if like is not None:
                like_count = like.like
            else:
                like_count = 0
            self.views['like_count'] = like_count
        except ObjectDoesNotExist:
            self.views['like_count'] = 0
        return render(request, 'movie-detail.html', self.views)


# @method_decorator(login_required, name='dispatch')
class CinemaHallView(BaseView):
    """
    This views Shows The All cinema hall of selected movie and it's showtime.
    """
    def get(self, request,pk,slug):
        # address = request.user.address
        self.views['pk'] = pk
        self.views['selected_date'] = Showtime.objects.get(pk = pk).show_date
        self.views['details'] = Movie.objects.get(slug=slug)
        movie_id = self.views['details'].id
        self.views['cinema_hall'] = CinemaHall.objects.prefetch_related('showtime_set').all()
        self.views['cin'] = {} 
        for cinema_hall in self.views['cinema_hall']:
            showtimes = cinema_hall.showtime_set.filter(movie=movie_id, show_date = self.views['selected_date'])
            self.views['cin'][cinema_hall] = showtimes
        return render(request, 'movie-showtime.html', self.views)
    
    
@method_decorator(login_required, name='dispatch')
class MovieLikeView(BaseView):
    """
    This views handle the like and unlike of user and display in page using Jquery Ajax
    """
    # @method_decorator(login_required,name='dispatch')
    def post(self, request):
        slug = request.POST.get('slug')
        
        print(slug)
        self.views['details'] = Movie.objects.prefetch_related('like_set').get(slug=slug)
        movie_id = self.views['details'].id
        try:
            
            like = self.views['details'].like_set.filter(movie=movie_id).order_by('liked_at').last()
            if like is not None:
                like_count = like.like
            else:
                like_count = 0
        except ObjectDoesNotExist:
            self.views['like_count'] = 0
        print("This is movie slug from ajax"+ slug)
        user = request.user
        movie = Movie.objects.get(slug = slug)
        movie_id = self.views['details'].id
        if Like.objects.filter(user=user , movie = movie_id).exists():
            Like.objects.filter(user=user , movie = movie_id).delete()
            try:
            
                like = self.views['details'].like_set.filter(movie=movie_id).order_by('liked_at').last()
                if like is not None:
                    like_count = like.like
                    
                else:
                    like_count = 0
            except ObjectDoesNotExist:
                like_count = 0
            res_data = {'message': 'Like deleted successfully', 'like':like_count}
            return JsonResponse(res_data)
        
        if Like.objects.filter(movie=movie_id).exists():
            count = Like.objects.get(movie = movie_id)
            ct = count.like
            
            Like.objects.create(user=user, movie=movie, like = ct + 1).save()
            try:
            
                like = self.views['details'].like_set.filter(movie=movie_id).order_by('liked_at').last()
                if like is not None:
                    like_count = like.like
                else:
                    like_count = 0
            except ObjectDoesNotExist:
                like_count = 0
            res_data = {'message':'Thank you for like ', 'like':like_count}
            return JsonResponse(res_data)
        else:
            Like.objects.create(user=user, movie=movie, like = 1).save()
            try:
            
                like = self.views['details'].like_set.filter(movie=movie_id).order_by('liked_at').last()
                if like is not None:
                    like_count = like.like
                else:
                    like_count = 0
            except ObjectDoesNotExist:
                like_count = 0
            res_data = {'message':'Thank you for Like', 'like':like_count}
            return JsonResponse(res_data)

