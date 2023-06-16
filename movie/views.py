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