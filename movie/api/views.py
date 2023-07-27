# from rest_framework.views import APIVie
from rest_framework.views import APIView
from rest_framework.response import Response
from movie.api.serializers import MovieSerializer, ShowtimeSerializer, MovieLikeSerializer
from rest_framework import status
from movie.models import Movie, Showtime, Like
from cinema.models import CinemaHall
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from movie.api.custom_authentication import CustomBasicAuthentication
# from django.



# Views for showing all movie and movie details 

class MovieAPIView(APIView):
    def get(self, request, slug = None):
        slug = slug
        if slug is not None:
            movie = Movie.objects.get(slug = slug)
            movie_serializer = MovieSerializer(movie)
            
            show_time = Showtime.objects.filter(show_date__gte = date.today(), movie = movie)
            show_date_queryset = show_time.order_by('show_date').distinct('show_date').values('pk', 'show_date')
            unique_pks = show_date_queryset.values_list('pk', flat=True)
            showtime_objects = Showtime.objects.filter(pk__in=unique_pks)
            showtime_serializer = ShowtimeSerializer(showtime_objects, many = True)
            
            response_data = {"Movie":movie_serializer.data,
                            "Show Date":showtime_serializer.data}
            # return Response(response_data, status = status.HTTP_200_OK)
        
        else:
            showing = Movie.objects.filter(active = "active",movie_status = 'showing')
            showing_serializer = MovieSerializer(showing,many = True)
            coming = Movie.objects.filter(active = "active",movie_status = 'comingsoon')
            coming_serializer = MovieSerializer(coming,many = True)
            
            response_data = {"showing":showing_serializer.data,
                            "coming":coming_serializer.data}
            # return Response( response_data)
        return Response(response_data, status=status.HTTP_200_OK)

# code for movie like
class MovieLikeAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, slug):
        try:
            movie = Movie.objects.prefetch_related('like_set').get(slug=slug)    
            like = movie.like_set.filter(movie=movie).order_by('liked_at').last()
            like_count = like.like
        except ObjectDoesNotExist:
            like_count = 0
        except Exception as e:
            like_count = 0
            print(e)
        return Response({'success':"Like Get methood", "like_count":like_count}, status=status.HTTP_200_OK)
    
    
    def post(self, request, slug):
        
        user = request.user
        slug = slug
        movie = Movie.objects.prefetch_related('like_set').get(slug=slug)
        
        data = {
            "user":user.id,
            'movie':movie.id
        }
        serializer = MovieLikeSerializer(data = data)    
        if serializer.is_valid():
            serializer.save()    
        return Response({'message':"success"}, status=status.HTTP_200_OK)
        
        


# views for showing Cinemahall And Showtime---------------------------
class CinemaShowtimeAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,slug,pk= None):
        # try:
        #     movie = Movie.objects.prefetch_related('showtime_set').get(slug = slug)
        #     selected_movie = MovieSerializer(movie)
        #     show_time = movie.showtime_set.objects.get(pk = pk)
        #     selected_date = show_time.show_date
        #     # show_date = ShowtimeSerializer(selected_date)
        #     cinema_hall_queryset = {}
        #     cinema_hall = CinemaHall.objects.prefetch_related('showtime_set').all()
        #     for cinema in cinema_hall:
        #         showtimes = cinema.showtime_set.filter(movie = movie, show_date = selected_date)
        #         cinema_hall_queryset[cinema.name] = ShowtimeSerializer(showtimes, many = True).data
            
            
            
        #     response_data = {
        #         "CinemaHall":cinema_hall_queryset,
        #         "Selcted_movie":selected_movie.data
        #     }
        try:
            movie = Movie.objects.get(slug=slug)
            selected_movie = MovieSerializer(movie)
            show_time = Showtime.objects.get(movie=movie, pk=pk)
            selected_date = show_time.show_date

            showtimes = Showtime.objects.filter(movie=movie.id, show_date=selected_date).prefetch_related('cinema_hall')

            cinema_hall_queryset = {}
            for showtime in showtimes:
                cinema_name = showtime.cinema_hall.name
                if cinema_name not in cinema_hall_queryset:
                    cinema_hall_queryset[cinema_name] = []
                cinema_hall_queryset[cinema_name].append(ShowtimeSerializer(showtime).data)

            response_data = {
                "CinemaHall": cinema_hall_queryset,
                "Selected_movie": selected_movie.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Showtime.DoesNotExist:
            return Response({'error': 'Showtime not found'}, status=status.HTTP_404_NOT_FOUND)
        


        
