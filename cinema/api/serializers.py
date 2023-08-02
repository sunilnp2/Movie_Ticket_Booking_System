from rest_framework import serializers
from cinema.models import CinemaHall

STATUS = [('active', 'active'), ('inactive', 'inactive')]


# Serializer for Ciemahall
class CinemaHallSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=100)
    slug = serializers.SlugField()
    hall_status = serializers.ChoiceField(STATUS, default='active')
    contact_number = serializers.CharField(max_length=200)
