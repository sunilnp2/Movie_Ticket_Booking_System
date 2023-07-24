from django.urls import path, include
app_name = 'movie'
from movie.views import *

urlpatterns = [
        path('search', MovieSearchView.as_view(), name = 'search'),
        path('filter', MovieFilterView.as_view(), name = 'filter'),
        path('movie', MovieView.as_view(), name='movie'),
        path('movie-detail/<slug>', MovieDetailView.as_view(), name='movie-detail'),
        path('cinemahall/<int:id>/<str:slug>', CinemaHallView.as_view(), name='cinemahall'),
        path('like/', MovieLikeView.as_view(), name='like'),
        
         # for api
        path('api/', include('authentication.api.urls')),
]
