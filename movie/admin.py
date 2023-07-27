from django.contrib import admin
from movie.models import *


# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'language', 'genre','movie_status']
    list_display_links = ['id', 'name', 'language', 'genre','movie_status']
   
admin.site.register(Movie, MovieAdmin)

from django import forms
class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = '__all__'
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ShowtimeAdmin(admin.ModelAdmin):
    form = ShowtimeForm
    list_display = ['id','show_date',  'start_time', 'end_time', 'shift', 'price']
    list_display_links = ['id','show_date', 'start_time', 'end_time', 'shift', 'price']
admin.site.register(Showtime, ShowtimeAdmin)


# admin.site.register(ShowDate, ShowDateAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'movie', 'like', 'liked_at']
    list_display_links = ['id', 'user', 'movie', 'like', 'liked_at']
    
admin.site.register(Like, LikeAdmin)
    