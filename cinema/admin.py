from django.contrib import admin
from cinema.models import *

class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    list_display_links = ('id', 'name', 'location')

admin.site.register(CinemaHall, CinemaHallAdmin)