from django.contrib import admin
from cinema.models import *

class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'status')
    list_display_links = ('id', 'name', 'location', 'status')

admin.site.register(CinemaHall, CinemaHallAdmin)