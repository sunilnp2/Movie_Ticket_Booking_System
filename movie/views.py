from django.shortcuts import render, redirect , get_object_or_404
from cinema.views import BaseView
from movie.models import *
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.forms import FilterMovieForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages

# Create your views here.


class MovieView(BaseView):
    def get(self, request):
        return render(request, 'movie.html', self.views)


class MovieSearchView(BaseView):
    def get(self, request):
        
        search = request.GET.get('search', None)
        
        
        if search is None:
            return redirect('movie:movie')
        elif search:
            mysearch = search.strip()
            self.views['search'] = Movie.objects.filter(
                name__icontains=mysearch)
            return render(request, 'movie-search.html', self.views)
        
       

class MovieFilterView(BaseView):
    def get(self, request):
        movies = Movie.objects.all()
        fm = FilterMovieForm(request.GET)
        if fm.is_valid():
            start_date = fm.cleaned_data['start_date']
            end_date = fm.cleaned_data['end_date']
            genre = fm.cleaned_data['genre']
            language = fm.cleaned_data['language']
            if len(genre) == 0:
                genre = None
            else:
                genre = [g for g in genre]
            
            q_objects = Q()
            for g in genre:
                q_objects |= Q(genre__icontains=g)
    
            # if start_date and end_date and language and genre:
            #     self.views['mov'] = movies.filter(
            #         release_date__gte=start_date, end_date__lte=end_date, language__icontains=language, genre__in=genre)

            # elif start_date and end_date:
            #     self.views['mov'] = movies.filter(
            #         release_date__gte=start_date, end_date__lte=end_date)
                
            if start_date:
                print("start date: %s" % start_date)
                self.views['mov'] = movies.filter(
                    release_date__gte=start_date)
            elif end_date:
                print("start date: %s" % end_date)
                self.views['mov'] = movies.filter(
                    end_date__lte=end_date)

            elif genre and language:
                self.views['mov'] = movies.filter(
                   q_objects, language__icontains=language)
                
            # Construct a dynamic Q object with logical OR conditions for genre__icontains
            elif genre:
                self.views['mov'] = movies.filter(q_objects)
                
            elif language is not None and language:
                print("I found language: %s" % language)
                self.views['mov'] = movies.filter(language__icontains=language)
            return render(request, 'movie-search.html', self.views)
        else:
            return redirect('conema:home')
        
        


class MovieDetailView(BaseView):
    def get(self, request, slug):
        self.views['details'] = Movie.objects.get(slug=slug)

        # code for showing dates
        self.views['dates'] = ShowDate.objects.filter(
            show_date__gte=date.today())
        self.views['hall_name'] = None
        self.views['selected_date'] = None
        
        movie_id = Movie.objects.get(slug = slug).id
        try:
            
            like = Like.objects.filter(movie=movie_id).order_by('liked_at').last()
            if like is not None:
                like_count = like.like
            else:
                like_count = 0
            self.views['like_count'] = like_count
        except ObjectDoesNotExist:
            self.views['like_count'] = 0
        return render(request, 'movie-detail.html', self.views)


@method_decorator(login_required, name='dispatch')
class CinemaHallView(BaseView):
    def get(self, request, id, slug):
        address = request.user.address
        self.views['d_id'] = id
        movie_id = Movie.objects.get(slug=slug).id
        movie = Movie.objects.prefetch_related('showtime_set').get(slug=slug)
        print(movie.showtime_set.filter(show_date__show_date = date.today()))
        self.views['details'] = Movie.objects.get(slug=slug)
        self.views['selected_date'] = ShowDate.objects.get(id=id)
        self.views['dates'] = ShowDate.objects.filter(
            show_date__gte=date.today())
        # self.views['hall'] = Showtime.objects.filter(show_date = id,movie = movie_id ).values('cinema_hall').distinct('cinema_hall')
        showtimes_queryset = Showtime.objects.filter(
            show_date=id, movie=movie_id)
        cinema_hall_ids = showtimes_queryset.values_list(
            'cinema_hall', flat=True).distinct()
        self.views['hall_name'] = CinemaHall.objects.filter(
            id__in=cinema_hall_ids, location__icontains=address)

        return render(request, 'movie-detail.html', self.views)


class MovieShowTimeView(BaseView):
    def get(self, request, d_id, h_id, slug):
        movie_id = Movie.objects.get(slug=slug).id
        self.views['hall_id'] = h_id
        self.views['details'] = Movie.objects.get(slug=slug)
        self.views['dates'] = ShowDate.objects.get(id=d_id)
        self.views['showtimes'] = Showtime.objects.filter(
            show_date=d_id, movie=movie_id, cinema_hall=h_id)

        return render(request, 'movie-showtime.html', self.views)
    

@method_decorator(login_required, name='dispatch')
class MovieLikeView(BaseView):
    def get(self, request, slug):
        user = request.user
        movie = Movie.objects.get(slug = slug)
        movie_id = movie.id
        if Like.objects.filter(user=user , movie = movie_id).exists():
            Like.objects.filter(user=user , movie = movie_id).delete()
            messages.error(request,"You Delete Your Like")
            return redirect('movie:movie-detail', slug)
        
        if Like.objects.filter(movie=movie_id).exists():
            count = Like.objects.get(movie = movie_id)
            ct = count.like
            
            Like.objects.create(user=user, movie=movie, like = ct + 1).save()
            messages.success(request, "Thank You For Like")
            return redirect('movie:movie-detail', slug)
        else:
            Like.objects.create(user=user, movie=movie, like = 1).save()
            messages.success(request, "Thank You For Like")
            return redirect('movie:movie-detail', slug)

