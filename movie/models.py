from django.db import models

# Create your models here.
MOVIE_STATUS  =(('showing', 'showing'), ('comingsoon', 'comingsoon'))
STATUS = (('active', 'active'), ('inactive', 'inactive'))
SHIFT = (('M', 'M'),('D', 'D'),('N', 'N'))

class Movie(models.Model):
    name = models.CharField(max_length=200)
    cast = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/')
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=200)
    release_date = models.DateField(blank=True,null=True)
    slug = models.SlugField(max_length=100)
    active = models.CharField(choices=STATUS, max_length=100, blank=True, null=True)
    status = models.CharField(choices=MOVIE_STATUS, max_length=100)
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.name

class MovieDate(models.Model):
    movie_date = models.DateField()

    def __str__(self):
        return str(self.movie_date)
    

class Showtime(models.Model):
    movie_date = models.ForeignKey(MovieDate, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift = models.CharField(choices=SHIFT, max_length=10)
    price = models.PositiveBigIntegerField()
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    def __str__(self):
        return self.shift
    