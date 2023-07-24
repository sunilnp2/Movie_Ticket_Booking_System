from django.db import models
from cinema.models import *
from authentication.models import User
# Create your models here.
MOVIE_STATUS  =(('showing', 'showing'), ('comingsoon', 'comingsoon'))
STATUS = (('active', 'active'), ('inactive', 'inactive'))
SHIFT = (('Morning', 'Morning'),('Day', 'Day'),('Night', 'Night'))


class Movie(models.Model):
    name = models.CharField(max_length=200)
    cast = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/')
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=200)
    release_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    slug = models.SlugField(max_length=100)
    active = models.CharField(choices=STATUS, max_length=100, blank=True, null=True)
    movie_status = models.CharField(choices=MOVIE_STATUS, max_length=100, blank=True, null=True)
    detail = models.TextField(blank=True)
    # like = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

class ShowDate(models.Model):
    show_date = models.DateField()

    def __str__(self):
        return str(self.show_date)


    
class Showtime(models.Model):
    show_date = models.ForeignKey(ShowDate, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift = models.CharField(choices=SHIFT, max_length=10)
    price = models.PositiveBigIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True                          )
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.shift
    
    
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    like = models.PositiveBigIntegerField(default = 0, null=True)
    liked_at  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['liked_at'] 
    
    def __str__(self):
        return self.user.username