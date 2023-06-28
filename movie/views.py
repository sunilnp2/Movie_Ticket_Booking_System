from django.shortcuts import render, redirect
from cinema.views import BaseView
from movie.models import *
from datetime import date
# Create your views here.

class MovieView(BaseView):
    def get(self, request):
        return render(request, 'movie.html', self.views)
    

class MovieSearchView(BaseView):
    def get(self,request):
        search = request.GET.get('search', None)
        if search:
            self.views['search'] = Movie.objects.filter(detail__icontains = search)
            return render(request, 'movie-search.html', self.views)
        return redirect('cinema:movie')
        

class MovieDetailView(BaseView):
    def get(self, request, slug):
        self.views['details'] = Movie.objects.get(slug = slug)

        # code for showing dates
        self.views['dates'] = ShowDate.objects.filter(show_date__gte = date.today())
        self.views['hall_name'] = None
        self.views['selected_date'] = None
        return render(request, 'movie-detail.html', self.views)

class CinemaHallView(BaseView):
    def get(self, request, id, slug):
        self.views['d_id'] = id
        movie_id = Movie.objects.get(slug = slug).id
        self.views['details'] = Movie.objects.get(slug = slug)
        self.views['selected_date'] = ShowDate.objects.get(id = id)
        self.views['dates'] = ShowDate.objects.filter(show_date__gte = date.today())
        # self.views['hall'] = Showtime.objects.filter(show_date = id,movie = movie_id ).values('cinema_hall').distinct('cinema_hall')
        showtimes_queryset = Showtime.objects.filter(show_date=id, movie=movie_id)
        cinema_hall_ids = showtimes_queryset.values_list('cinema_hall', flat=True).distinct()
        self.views['hall_name'] = CinemaHall.objects.filter(id__in=cinema_hall_ids)


        return render(request,'movie-detail.html',self.views) 

    

class MovieShowTimeView(BaseView):
    def get(self, request, d_id,h_id, slug):
        movie_id = Movie.objects.get(slug = slug).id
        self.views['hall_id'] = h_id
        self.views['details'] = Movie.objects.get(slug = slug)
        self.views['dates'] = ShowDate.objects.get(id = d_id)
        self.views['showtimes'] = Showtime.objects.filter(show_date = d_id,movie = movie_id,cinema_hall = h_id)

        return render(request, 'movie-showtime.html', self.views)


