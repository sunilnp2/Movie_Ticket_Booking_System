from django.contrib import admin
from movie.models import *


# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'language', 'genre','status']
    list_display_links = ['id', 'name', 'language', 'genre','status']
   
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
    list_display = ['id',  'start_time', 'end_time', 'shift', 'price']
    list_display_links = ['id', 'start_time', 'end_time', 'shift', 'price']
admin.site.register(Showtime, ShowtimeAdmin)


class MovieDateAdmin(admin.ModelAdmin):
    list_display = ('id','movie_date')
admin.site.register(MovieDate, MovieDateAdmin)