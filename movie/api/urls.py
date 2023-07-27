from django.urls import path
from movie.api.views import MovieAPIView, CinemaShowtimeAPIView, MovieLikeAPIView

urlpatterns = [
    path('movie_list/',MovieAPIView.as_view(), name='movie_list'),
    path('movie_list/<str:slug>',MovieAPIView.as_view(), name='movie_list'),
    
    path('cinshowtime/<str:slug>/<int:pk>/', CinemaShowtimeAPIView.as_view(), name='cinshowtime'),
    path('api_like/<str:slug>',MovieLikeAPIView.as_view(),name='api_like'),
]

