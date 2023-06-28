from django.urls import path
app_name = 'movie'
from movie.views import *

urlpatterns = [
        path('search', MovieSearchView.as_view(), name = 'search'),
        path('movie', MovieView.as_view(), name='movie'),
        path('movie-detail/<slug>', MovieDetailView.as_view(), name='movie-detail'),
        path('showtime/<int:d_id>/<int:h_id>/<str:slug>', MovieShowTimeView.as_view(), name='showtime'),
        path('cinemahall/<int:id>/<str:slug>', CinemaHallView.as_view(), name='cinemahall'),
    
]
