from rest_framework.views import APIView
from rest_framework.response import Response
from movie.api.serializers import MovieSerializer
from rest_framework import status
from movie.models import Movie

class HomeAPiView(APIView):
    def get(self, request):
        showing = Movie.objects.filter(active = "active",movie_status = 'showing')
        showing_serializer = MovieSerializer(showing,many = True)
        coming = Movie.objects.filter(active = "active",movie_status = 'comingsoon')
        coming_serializer = MovieSerializer(coming,many = True)
        
        response_data = {"showing":showing_serializer.data,
                         "coming":coming_serializer.data}
        return Response( response_data, status = status.HTTP_202_ACCEPTED)



