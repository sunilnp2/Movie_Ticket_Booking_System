
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from movie.models import Movie, Like
from movie.models import MOVIE_STATUS, STATUS, SHIFT
from cinema.models import CinemaHall
from authentication.models import User
from django.utils import timezone

# serializer for Showiing Movie----------------------------------------

class MovieSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    cast = serializers.CharField(max_length=200)
    duration = serializers.CharField(max_length=50)
    image = serializers.ImageField()
    genre = serializers.CharField(max_length=100)
    language = serializers.CharField(max_length=200)
    release_date = serializers.DateField(allow_null=True, required=False)
    end_date = serializers.DateField(allow_null=True, required=False)
    slug = serializers.SlugField(max_length=100)
    active = serializers.ChoiceField(choices=STATUS, allow_null=True, required=False)
    movie_status = serializers.ChoiceField(choices=MOVIE_STATUS, default='showing')
    detail = serializers.CharField(allow_blank=True, required=False)
    trailer_link = serializers.URLField(allow_null=True, allow_blank=True)
    
    


# serializer for Showtime
class ShowtimeSerializer(serializers.Serializer):
    show_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    shift = serializers.ChoiceField(choices=SHIFT)
    price = serializers.IntegerField()
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), allow_null=True, required=False)
    cinema_hall_id = serializers.PrimaryKeyRelatedField(queryset=CinemaHall.objects.all(), allow_null=True, required=False)


# serializer for MovieLike

class MovieLikeSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset = Movie.objects.all())
    like = serializers.IntegerField(default = 0)
    liked_at = serializers.DateTimeField(default=timezone.now)
    
    def create(self, validated_data):
        user = validated_data.get('user')
        movie = validated_data.get('movie') 
        # like = validated_data.get('like')
        
        if Like.objects.filter(user = user, movie = movie).exists():
                Like.objects.filter(user = user , movie = movie).delete()
                return 'Delete Done'
                
        elif Like.objects.filter(movie=movie).exists():
            count = Like.objects.get(movie = movie)
            ct = count.like
            Like.objects.create(user = user, movie = movie, like = ct + 1).save()
            return 'Save'
            
        else:
            Like.objects.create(user=user, movie=movie, like = 1).save()
            return 'Save'
   